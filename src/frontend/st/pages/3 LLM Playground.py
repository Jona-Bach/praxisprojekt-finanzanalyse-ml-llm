import os
import time
import requests
import streamlit as st
import pandas as pd
import numpy as np
from backend.data_processing.alphavantage_processed import get_processed_table
from backend.database.users_database import get_user_table, list_user_tables
from backend.database.db_functions import get_all_yf_price_history, get_yf_pricing_raw

# __________________________Header____________________________

st.set_page_config(page_title="LLM Playground", page_icon="🤖", layout="wide")

# -----------------------------
# Helper Functions - Ollama
# -----------------------------
def base_url_from_choice(choice: str, custom: str | None = None) -> str:
    if choice == "Container":
        return "http://ollama:11434"
    if choice == "Host":
        return "http://host.docker.internal:11434"
    if choice == "Local" and custom:
        return custom.strip().rstrip("/")
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def check_connection(base_url: str, timeout: float = 3.0) -> tuple[bool, str]:
    """Checks if Ollama is reachable at base_url."""
    try:
        r = requests.get(f"{base_url}/api/version", timeout=timeout)
        if r.ok:
            return True, f"Connected to Ollama @ {base_url} (Version: {r.json().get('version', 'unknown')})"
        return False, f"No OK response from {base_url} (Status {r.status_code})"
    except Exception as e:
        return False, f"No connection to {base_url}: {e}"


def ensure_model(base_url: str, model: str, timeout: float = 120.0) -> None:
    """Ensures that a model is available."""
    try:
        resp = requests.post(
            f"{base_url}/api/pull",
            json={"name": model, "stream": False},
            timeout=timeout,
        )
    except Exception as e:
        st.info(f"Model '{model}' could not be automatically loaded: {e}")


def generate_once(base_url: str, model: str, prompt: str, timeout: float = 120.0) -> str:
    """Single text generation (no streaming response)."""
    r = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")


# -----------------------------
# Helper Functions - Data
# -----------------------------
def _try_parse_numeric_series(s: pd.Series) -> pd.Series | None:
    """Attempts to robustly convert a string series to floats."""
    s = s.astype(str).str.strip()
    s = s.replace({"": np.nan, "-": np.nan, "NA": np.nan, "NaN": np.nan})

    frac_digit = s.str.contains(r"\d", regex=True).mean()
    if frac_digit < 0.5:
        return None

    s_clean = (
        s.str.replace("%", "", regex=False)
         .str.replace("€", "", regex=False)
         .str.replace("$", "", regex=False)
         .str.replace(" ", "", regex=False)
    )

    cand1 = pd.to_numeric(s_clean, errors="coerce")
    s_de = s_clean.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    cand2 = pd.to_numeric(s_de, errors="coerce")

    ratio1 = cand1.notna().mean()
    ratio2 = cand2.notna().mean()

    best_ratio = max(ratio1, ratio2)
    if best_ratio < 0.5:
        return None

    return cand1 if ratio1 >= ratio2 else cand2


def auto_convert_numeric_and_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Converts string columns to float/datetime."""
    df = df.copy()

    for col in df.columns:
        col_series = df[col]

        if pd.api.types.is_numeric_dtype(col_series) or np.issubdtype(col_series.dtype, np.datetime64):
            continue

        col_lower = col.lower()

        if any(k in col_lower for k in ["date", "time", "timestamp"]):
            dt = pd.to_datetime(col_series, errors="coerce")
            if dt.notna().mean() > 0.5:
                df[col] = dt
                continue

        parsed = _try_parse_numeric_series(col_series)
        if parsed is not None:
            df[col] = parsed

    return df


@st.cache_data
def load_data_from_source(
    source: str,
    symbol: str = None,
    table_name: str = None,
):
    """Loads data depending on selected source."""
    if source == "Price History":
        df = get_all_yf_price_history()
    elif source == "Single Stock Price":
        if not symbol:
            return pd.DataFrame()
        df = get_yf_pricing_raw(symbol)
    elif source == "Alphavantage":
        if not table_name:
            return pd.DataFrame()
        df = get_processed_table(table_name)
    elif source == "User Tables":
        if not table_name:
            return pd.DataFrame()
        df = get_user_table(table_name)
    else:
        df = pd.DataFrame()

    if df is not None and not df.empty:
        df = auto_convert_numeric_and_datetime(df)

    return df


def build_prediction_prompt(
    prediction_type: str,
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    sample_size: int = 10
) -> str:
    """Creates the prompt for the LLM based on prediction type and data."""
    
    # Prepare data sample
    df_sample = df[feature_cols + [target_col]].tail(sample_size)
    data_str = df_sample.to_string(index=False)
    
    # Statistics
    stats_str = df[feature_cols + [target_col]].describe().to_string()
    
    # Base prompt depending on type
    if prediction_type == "Regression (predict numerical value)":
        prompt = f"""You are a financial analyst with expertise in quantitative analysis. 

TASK: Analyze the following financial data and create a well-founded prediction for '{target_col}'.

AVAILABLE FEATURES:
{', '.join(feature_cols)}

CURRENT DATA (last {sample_size} rows):
{data_str}

STATISTICS:
{stats_str}

INSTRUCTIONS:
1. Analyze the trends and patterns in the features
2. Identify relevant correlations with the target '{target_col}'
3. Provide a concrete numerical prediction for the next value of '{target_col}'
4. Justify your prediction briefly and concisely
5. State a confidence interval (min-max range)

FORMAT:
Prediction: [numerical value]
Confidence Interval: [min] - [max]
Justification: [Your analysis]"""

    elif prediction_type == "Classification (predict category)":
        unique_values = df[target_col].unique()[:10]
        prompt = f"""You are a financial analyst with expertise in classification tasks.

TASK: Analyze the following data and classify the next value of '{target_col}'.

AVAILABLE FEATURES:
{', '.join(feature_cols)}

POSSIBLE CATEGORIES FOR '{target_col}':
{', '.join(map(str, unique_values))}

CURRENT DATA (last {sample_size} rows):
{data_str}

STATISTICS:
{stats_str}

INSTRUCTIONS:
1. Analyze the patterns in the features
2. Identify which features influence the classification
3. Choose the most likely category for the next value
4. Justify your choice with concrete observations from the data
5. Provide probabilities for the top 3 categories (if possible)

FORMAT:
Prediction: [category]
Probability: [percent]
Alternative Categories: [category 2] ([percent]), [category 3] ([percent])
Justification: [Your analysis]"""

    elif prediction_type == "Trend Analysis (predict direction)":
        prompt = f"""You are a financial analyst with expertise in trend analysis.

TASK: Analyze the trends and predict whether '{target_col}' will rise, fall, or remain stable.

AVAILABLE FEATURES:
{', '.join(feature_cols)}

CURRENT DATA (last {sample_size} rows):
{data_str}

STATISTICS:
{stats_str}

INSTRUCTIONS:
1. Identify the current trend in '{target_col}'
2. Analyze how the features influence the trend
3. Predict whether the trend will continue, reverse, or stagnate
4. Classify as: RISING, FALLING, or STABLE
5. Justify your prediction with momentum indicators and feature analysis

FORMAT:
Trend Prediction: [RISING/FALLING/STABLE]
Confidence: [High/Medium/Low]
Expected Change: [percent or absolute value]
Justification: [Your analysis with technical indicators]"""

    else:  # Free Analysis
        prompt = f"""You are a financial analyst with broad expertise.

TASK: Conduct a comprehensive analysis of the following data.

AVAILABLE FEATURES:
{', '.join(feature_cols)}

TARGET VARIABLE:
{target_col}

CURRENT DATA (last {sample_size} rows):
{data_str}

STATISTICS:
{stats_str}

INSTRUCTIONS:
1. Analyze data quality and completeness
2. Identify patterns, trends, and anomalies
3. Examine correlations between features and target
4. Provide assessments on predictability
5. Recommend further analysis steps or feature engineering

Create a structured, detailed analysis."""

    return prompt


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🤖 LLM Playground with Data Analysis")

st.caption("""
Use Ollama LLMs for intelligent financial analysis and predictions based on your data.
""")

# -----------------------------
# Sidebar: Ollama Configuration
# -----------------------------
with st.sidebar:
    st.header("⚙️ Ollama Settings")
    
    choice = st.radio(
        "Choose source:",
        options=["Container", "Host", "Local"],
        index=0,
        horizontal=True,
    )

    custom_url = None
    if choice == "Local":
        custom_url = st.text_input("Local Ollama URL:", value="http://localhost:11434")

    base_url = base_url_from_choice(choice, custom_url)
    st.code(base_url, language=None)

    if st.button("🔌 Test connection"):
        ok, msg = check_connection(base_url)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    st.divider()
    
    model = st.text_input("Model name:", value="mathstral:7b")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔽 Load Model"):
            with st.spinner(f"Loading model '{model}'..."):
                ensure_model(base_url, model, timeout=120)
                st.success(f"✓ Model '{model}' loaded!")
    with col_b:
        timeout_s = st.number_input("Timeout (s)", min_value=5, max_value=600, value=120, help="Timeout determines how long to wait for the model's response (should be increased for downloads)")
    
    auto_pull = st.toggle("Auto-load on analysis", value=True, 
                          help="Automatically load model if not available")

    st.divider()
    
    # Data source
    st.header("📊 Data Source")
    
    data_source = st.selectbox(
        "Data source",
        [
            "No Table selected",
            "Price History",
            "Single Stock Price",
            "Alphavantage",
            "User Tables",
        ]
    )

    symbol = None
    table_name = None

    if data_source == "Single Stock Price":
        symbol = st.text_input("Symbol (e.g. AAPL)", value="AAPL")
    elif data_source == "No Table selected":
        st.info("Select a table")
    elif data_source == "Alphavantage":
        ALPHAVANTAGE_TABLES = [
            "alphavantage_pricing_processed",
            "alphavantage_processed_kpi",
        ]
        table_name = st.selectbox("Alphavantage table", ALPHAVANTAGE_TABLES)
    elif data_source == "User Tables":
        user_tables = list_user_tables()
        if user_tables:
            table_name = st.selectbox("User Table", user_tables)
        else:
            st.warning("No tables found")
            table_name = None

# -----------------------------
# Main Area: Data Selection & Analysis
# -----------------------------

# Load data
with st.spinner("Loading data..."):
    df = load_data_from_source(data_source, symbol=symbol, table_name=table_name)

if df is None or df.empty:
    st.warning("⚠️ No data loaded. Please select a data source.")
    st.stop()

# Data overview
st.subheader("📊 Data Overview")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Rows", len(df))
with c2:
    st.metric("Columns", df.shape[1])
with c3:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    st.metric("Numeric Columns", len(numeric_cols))

with st.expander("📋 Show DataFrame", expanded=False):
    st.dataframe(df.head(50), width="stretch")

# Feature & Target Selection
st.divider()
st.subheader("🎯 Feature & Target Selection")

all_cols = df.columns.tolist()

col1, col2 = st.columns([2, 1])

with col1:
    feature_cols = st.multiselect(
        "Feature columns (X)",
        options=all_cols,
        default=[c for c in numeric_cols if c != "target"][:5],
        help="Select the columns that should serve as input for the analysis"
    )

with col2:
    target_col = st.selectbox(
        "Target column (y)",
        options=all_cols,
        help="The variable to be predicted"
    )

# Prediction Configuration
st.divider()
st.subheader("🔮 Prediction Configuration")

col_pred1, col_pred2 = st.columns(2)

with col_pred1:
    prediction_type = st.selectbox(
        "Prediction type",
        [
            "Regression (predict numerical value)",
            "Classification (predict category)",
            "Trend Analysis (predict direction)",
            "Free Analysis",
        ],
        help="Choose what type of analysis the LLM should perform"
    )

with col_pred2:
    sample_size = st.slider(
        "Data sample size",
        min_value=5,
        max_value=50,
        value=10,
        help="Number of last rows to be sent to the LLM"
    )

# Custom prompt (optional)
with st.expander("✏️ Add custom prompt (optional)"):
    custom_prompt_addition = st.text_area(
        "Additional instructions for the LLM:",
        placeholder="e.g.: Pay special attention to macroeconomic factors...",
        height=100
    )

# Generate Button
st.divider()

if not feature_cols:
    st.warning("⚠️ Please select at least one feature column.")
elif not target_col:
    st.warning("⚠️ Please select a target column.")
else:
    if st.button("🪄 Start LLM Analysis", type="primary", width="stretch"):
        # Check connection
        ok, msg = check_connection(base_url)
        if not ok:
            st.error(f"❌ Cannot connect: {msg}")
            st.stop()
        
        st.success(msg)
        
        # Load model
        if auto_pull:
            with st.status(f"Loading model '{model}'...", expanded=False) as status:
                ensure_model(base_url, model, timeout=timeout_s)
                status.update(label=f"✓ Model '{model}' ready", state="complete")
        
        # Create prompt
        with st.spinner("Creating analysis prompt..."):
            base_prompt = build_prediction_prompt(
                prediction_type=prediction_type,
                df=df,
                feature_cols=feature_cols,
                target_col=target_col,
                sample_size=sample_size
            )
            
            if custom_prompt_addition:
                full_prompt = f"{base_prompt}\n\nADDITIONAL INSTRUCTIONS:\n{custom_prompt_addition}"
            else:
                full_prompt = base_prompt
        
        # Show prompt (optional)
        with st.expander("📝 Show generated prompt"):
            st.code(full_prompt, language="text")
        
        # Generate
        with st.status("🤖 LLM generating analysis...", expanded=True) as status:
            try:
                t0 = time.time()
                response = generate_once(base_url, model, full_prompt, timeout=timeout_s)
                dt = time.time() - t0
                
                status.update(label=f"✓ Analysis completed in {dt:.2f}s", state="complete")
                
                # Display result
                st.divider()
                st.subheader("📊 LLM Analysis Result")
                st.markdown(response)
                
                # Metadata
                with st.expander("ℹ️ Analysis Details"):
                    st.write(f"**Model:** {model}")
                    st.write(f"**Prediction type:** {prediction_type}")
                    st.write(f"**Data source:** {data_source}")
                    st.write(f"**Features:** {', '.join(feature_cols)}")
                    st.write(f"**Target:** {target_col}")
                    st.write(f"**Generation time:** {dt:.2f}s")
                    st.write(f"**Sample size:** {sample_size} rows")
                
            except requests.HTTPError as http_err:
                st.error(f"❌ HTTP error: {http_err.response.status_code}")
                st.code(http_err.response.text)
            except Exception as e:
                st.error(f"❌ Error during generation: {e}")