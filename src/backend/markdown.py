def markdown_setup():
    md = """# 🚀 Setup Guide

Welcome to **FinSight** – your comprehensive tool for comparing traditional regression methods with LLM-based prediction models for financial data.

---

## 🔧 **Initial Setup**

### **Option 1: Docker Deployment (Recommended)**

1. **Prerequisites:**
   - Install Docker and Docker Compose on your system
   - Ensure ports 8501 (Streamlit) and 11434 (Ollama) are available

2. **Start the Application:**
   ```bash
   docker-compose up -d
   ```
   This will start:
   - Streamlit frontend (accessible at `http://localhost:8501`)
   - Ollama container for LLM functionality

3. **Access the Application:**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will automatically connect to the containerized Ollama instance

### **Option 2: Local Deployment**

1. **Prerequisites:**
   - Python 3.8 or higher
   - Install Ollama locally from [ollama.com](https://ollama.com)

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Application:**
   ```bash
   python3 -m src.backend.launch
   ```

4. **Configure Ollama Connection:**
   - Go to **Settings → Global Settings**
   - Enable "Local Ollama" toggle
   - Enter your Ollama URL (default: `http://localhost:11434`)
   - Click "Test connection" to verify

---

## ⚙️ **Required Configuration**

### **1. Ollama Setup (LLM Backend)**

**Why needed:** All LLM features (LLM Playground, Assistant) require Ollama.

**Setup Steps:**

#### **For Docker Users:**
- **No action required** – Ollama runs automatically in the container
- Default connection: `http://ollama:11434`

#### **For Local Installation:**
1. Navigate to **Settings → Assistant Settings**
2. Select "Local Ollama" under "Change Source"
3. Test the connection
4. Download a model (recommended: `phi3:mini` for lightweight or `llama3.1:8b` for better quality)

**Model Selection:**
- Go to **Settings → Assistant Settings → Assistant Model Management**
- Choose from suggested models or enter a custom model name
- Click "⬇️ Download" to install the model
- Wait for download completion (may take several minutes depending on model size)

**Available Models:**
| Model | Size | Best For |
|-------|------|----------|
| phi3:mini | 3.8B | Lightweight tasks, fast responses |
| llama3.1:8b | 8B | General-purpose, good quality |
| llama3.2:3b | 3B | Low-resource environments |
| mistral | 7B | Balanced performance |
| qwen2 | up to 72B | Complex tasks, multilingual |

### **2. Alpha Vantage API Key (Data Downloads)**

**Why needed:** Required for downloading stock data and updating ticker information.

**How to get:**
1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Register for a free API key
3. Copy your key

**Configuration:**
1. Go to **Settings → Global Settings → Alphavantage Key**
2. Paste your API key into the input field
3. Click "Set Alphavantage Key!"

**⚠️ Important:**
- The key is stored **only for the current session** (security measure)
- You need to re-enter it after restarting the application
- Free tier limits: 5 API calls per minute, 500 per day

### **3. Initial Ticker List (Optional but Recommended)**

**Why configure:** Define which stocks are loaded by default.

**Setup Steps:**
1. Go to **Settings → Data Settings → Initial Tickers loading**
2. **Option A:** Use the default ticker list (400+ US stocks)
3. **Option B:** Create custom list:
   - Select tickers from the dropdown
   - Add custom tickers (comma-separated) in the text field
   - Click "Choose as New Initial Tickers"
4. Click "Load initial Data" to download the selected stocks
5. Make sure under "Analysis Settings, the timeperiod is set correctly!"

---

## 📊 **First Steps After Setup**

### **Step 1: Update Data**
1. Navigate to **Data** page
2. Ensure your Alpha Vantage key is set (Settings → Global Settings)
3. Click "Update All Data" in the sidebar
4. Wait for download to complete (may take time due to API limits)
5. Check "Last data update" timestamp to verify

### **Step 2: Verify Ollama Connection**
1. Go to **Assistant** page
2. Check the connection status box:
   - ✅ Green: "Connected with Ollama @ ..." → Ready to use
   - ❌ Red: Connection error → Go to Settings and fix Ollama configuration
3. Test the assistant by asking: "How do I use this application?"

### **Step 3: Test Features**
1. **Data Analysis:**
   - Go to **Data → Single Stock Analysis**
   - Select a ticker (e.g., AAPL)
   - View company info and charts
2. **Machine Learning:**
   - Go to **Machine Learning**
   - Choose a data source
   - Select features and target
   - Train a simple model
3. **LLM Playground:**
   - Go to **LLM Playground**
   - Test connection in sidebar
   - Load a model if needed
   - Run a simple analysis

---

## 📊 **Data**

The Data page is your starting point for stock analysis and data management.

### **Single Stock Analysis**
Analyze individual stocks in detail:
- Current metrics and fundamental data
- Price development with interactive charts
- Historical performance metrics

### **Compared Stock Analysis**
Compare multiple stocks directly to identify relative performance and correlations.

### **Sidebar Functions**

#### 🔄 **Update All Data**
Automatically downloads the latest information for all stocks marked as "Initial" in your ticker list.

#### 📦 **Update Processed Data**
Manually transfers metrics into the processed database (only necessary if automatic processing fails).

#### 🎯 **Update Single Ticker Data**
Update specific tickers from your existing list. *Note: Check the last update timestamp to know your data status.*

#### 📥 **Download Ticker Data**
Search for and download new stocks into your database.

**⚠️ Important:** All download functions require an **Alpha Vantage API Key**, which must be configured under **Settings → Global Settings** (stored only for the current session).

### **Create Your Own Database**
Create custom databases from Excel or CSV files:
- Drag and drop or browse files (CSV, Excel, up to 200MB)
- Assign individual database names
- Choose conflict strategy:
  - **Fail:** Abort if table exists (safe)
  - **Replace:** Overwrite existing data (destructive)
  - **Append:** Add new rows to existing table
- Manage created databases under **Settings → Data Settings → Clear Table**

---

## 🤖 **Machine Learning**

### **ML Studio**
Build your own machine learning models with the following options:

**Sidebar Configuration:**
- **Algorithm:** Choose from Linear Regression, Decision Tree, Random Forest, Logistic Regression, or Direction Classification
- **Data Source:** Select from Price History, Single Stock, Alphavantage, or User Tables
- **Test Set Size:** Adjust train/test split (default: 20%)
- **Feature Scaling:** Enable StandardScaler for normalization
- **Time Series Mode:** Generate lag features automatically

**Main Area:**
- Select feature columns (X) – multiple selection allowed
- Choose target column (y) – single selection
- Optional: Configure Forecast Horizon (1 Day, 3 Weeks, 3 Months, 1 Year)
- Click "🚀 Train Model" to start training

**Available Algorithms:**
- **Linear Regression:** Fast, interpretable, good for linear relationships
- **Decision Tree Regressor:** Non-linear patterns, risk of overfitting
- **Random Forest Regressor:** Robust ensemble method, handles complex patterns
- **Logistic Regression:** For classification tasks with discrete targets
- **Direction Classification:** Binary prediction (price up/down)

⚠️ **Note:** The program executes algorithms without validation. Selecting an appropriate algorithm for your data is your responsibility!

### **Results and Evaluation**
After training, view:
- **Regression:** RMSE, MSE, R² metrics + Actual vs. Predicted plot
- **Classification:** Accuracy + Confusion Matrix

### **Model Management**
In the "Saved Models" tab, you can:
- View all saved models with metadata
- Download models for external use (`.pkl` files)
- Test models with new data
- Delete old models

---

## 🧠 **LLM Playground**

Leverage the power of Large Language Models for financial predictions:

**Sidebar Configuration:**

1. **Ollama Settings:**
   - Choose source: Container (Docker) / Host / Local
   - Test connection before starting
   - Enter model name (e.g., `mathstral:7b`)
   - Click "🔽 Load Model" if not available
   - Set timeout (default: 120s)
   - Enable "Auto-load on analysis" for convenience

2. **Data Source:**
   - Same options as ML Studio
   - Select table or ticker

**Main Area Configuration:**

1. **Feature & Target Selection:**
   - Select feature columns (X)
   - Choose target column (y)

2. **Prediction Configuration:**
   - **Prediction Type:** Choose analysis mode
     - **Regression:** Predict numerical values with confidence intervals
     - **Classification:** Categorize into discrete classes
     - **Trend Analysis:** Predict direction (rising/falling/stable)
     - **Free Analysis:** Open-ended data exploration
   - **Data Sample Size:** Number of rows sent to LLM (5-50)

3. **Custom Prompt (Optional):**
   - Add specific instructions
   - Example: "Pay special attention to macroeconomic factors"

4. **Start Analysis:**
   - Click "🪄 Start LLM Analysis"
   - Wait for model to generate response
   - View results with metadata (model, time, features used)
   - Inspect generated prompt for transparency

💡 **Recommendation:** Use mathematically specialized models like **MathStral 7B** for optimal results with financial calculations. Better resources and larger models significantly improve prediction quality and accuracy.

---

## 💬 **Assistant**

An integrated AI assistant is available to help you navigate and use the platform.

**How to Use:**
1. Verify Ollama connection (green status box)
2. Type your question in the chat field
3. Wait for response (may take 10-60 seconds depending on model)
4. Continue conversation or reset chat

**Common Questions:**
- "How do I train a model?"
- "What does Forecast Horizon mean?"
- "How do I interpret R² values?"
- "Why is my LLM analysis not working?"

**Configuration:** 
- Go to **Settings → Assistant Settings**
- Select model (default: `llama3.1:8b`)
- Choose Ollama source (local/container)
- Download model if not installed

---

## ⚙️ **Settings**

### **Global Settings**
- **Local Ollama Toggle:** Enable for local Ollama installation (disable for Docker)
- **Local Ollama URL:** Custom URL for local instance (default: `http://localhost:11434`)
- **Test Connection:** Verify Ollama accessibility
- **Set as Standard:** Save URL as default
- **Reset Ollama Config:** Clear saved settings
- **Alpha Vantage API Key:** Enter key for data downloads (session-only storage)

### **Data Settings**

1. **Clear Table:**
   - Select table from dropdown (system or user tables)
   - Click "Clear Table"
   - Confirm deletion (⚠️ irreversible!)

2. **Initial Tickers Loading:**
   - **Load Initial Data:** Download data for selected tickers
   - **Create New List:** 
     - Select from 400+ known tickers
     - Add custom tickers (comma-separated)
     - Click "Choose as New Initial Tickers"
   - **Manage List:**
     - Add to existing list
     - Remove selected tickers
     - Delete entire custom list

3. **Analysis Settings:**
   - **Earliest Date:** Set historical data range (default: 2020-01-01)
   - Reduces download time and storage for shorter periods
   - Click "Save new Date!" to apply

### **Assistant Settings**

1. **Change Source:**
   - Local Ollama (for local installation)
   - Ollama Container (for Docker deployment)

2. **Model Management:**
   - View list of recommended models with specs
   - Select from dropdown or enter custom model
   - Download model (⬇️ button)
   - Wait for installation (1-10 minutes depending on size)
   - Status indicator: ✔ installed / ❌ not installed

**Model Recommendations:**
- **For Speed:** phi3:mini (3.8B) – Fast but basic
- **Balanced:** llama3.1:8b (8B) – Good quality, reasonable speed
- **Best Quality:** qwen2 (72B) – Requires powerful hardware

---

## 🎯 **Best Practices**

1. **API Key Security:** The Alpha Vantage key is only stored temporarily during your session
2. **Check Data Status:** Regularly review the update timestamps of your tickers
3. **Model Selection:** Larger, specialized models deliver better results but require more resources
4. **Resource Management:** Use row limits in ML Studio to optimize performance
5. **Custom Databases:** Test different data combinations for personalized analyses
6. **Ollama Connection:** Always test your Ollama connection before starting analyses
7. **Rate Limits:** Be mindful of Alpha Vantage limits (5 calls/minute, 500/day)
8. **Data Quality:** Check data completeness before training models

---

## 🔧 **Technical Notes**

- All LLM functions use **Ollama** as backend
- When running without Docker, select "Local Ollama" in the settings
- For external Ollama instances, use IP-based configuration
- The platform executes calculations without logic validation – method selection is the user's responsibility
- LLM responses are qualitative and non-deterministic
- Larger datasets may cause loading delays
- Session state is not persistent across restarts
- User databases are stored in `users_database.db`
- System databases are in `data/` directory

---

## 📚 **Recommended Workflow**

1. **Initial Setup:**
   - Start application (Docker or local)
   - Configure Ollama connection
   - Download Assistant model
   - Enter Alpha Vantage API key

2. **Load Data:**
   - Set initial ticker list (Settings)
   - Click "Load initial Data"
   - Execute "Update All Data"
   - Verify data in Database tab

3. **Exploration:**
   - Use Single Stock Analysis to verify data quality
   - Test Compared Stock Analysis
   - Familiarize with available metrics

4. **Modeling:**
   - Experiment with ML Studio (simple model first)
   - Try LLM Playground with different prediction types
   - Compare results between ML and LLM

5. **Iteration:**
   - Refine features based on results
   - Test different algorithms
   - Adjust sample sizes and parameters
   - Save successful models

---

## 🆘 **Troubleshooting**

### **Ollama Connection Failed**
- Docker: Ensure container is running (`docker ps`)
- Local: Check if Ollama is installed and running
- Verify URL in Settings → Global Settings
- Test connection button should show green status

### **Assistant Not Responding**
- Check Ollama connection status
- Verify model is downloaded (Settings → Assistant Settings)
- Try smaller model if timeout occurs
- Increase timeout in LLM Playground settings

### **Data Download Fails**
- Verify Alpha Vantage API key is entered
- Check if rate limit is exceeded (wait 1 minute)
- Ensure internet connection
- Check ticker symbol is valid

### **ML Training Errors**
- Verify data source is loaded (check row count > 0)
- Ensure features and target are selected
- Check for NaN values in data
- Verify minimum row requirement is met (Settings → ML Settings)

### **LLM Analysis Takes Too Long**
- Use smaller model (phi3:mini instead of llama3.1:8b)
- Reduce data sample size
- Increase timeout in sidebar
- Check system resources (RAM/CPU usage)

---

## 🆘 **Getting Help**

- Use the **Assistant** page for questions about the application
- Check the **Database** tab on the Data page to verify data availability
- Review **Settings** to ensure correct configuration
- Test Ollama connection before using LLM features
- Check console logs for detailed error messages

---

**Good luck with your financial analyses! 📈**"""
    return md

def markdown_welcome():

    md = """## Welcome to FinSight 👋

FinSight helps you analyze stocks and compare **traditional regression-based models** with **LLM-powered forecasting**, all in one dashboard. Use it to explore market data, manage your ticker database, and test different prediction approaches on financial time series.

### What you can do here

- **Stock Data & Analysis**
  - Review key metrics, fundamentals, interactive price charts, and historical performance.
  - Compare two stocks side-by-side to understand relative performance and correlation.
  - Keep your dataset up to date (bulk updates or individual tickers) and download new tickers into your database.

- **Build Your Own Database**
  - Import Excel/CSV files to create custom datasets.
  - Choose whether to replace existing databases and manage them in **Settings → Data Settings**.

- **Machine Learning Studio**
  - Train baseline models by selecting features, defining a target, choosing an algorithm, and optionally enabling time-series mode or scaling.
  - Manage saved models, download them, and test them on new data.

- **LLM Playground**
  - Create prompt-driven forecasts using selected data columns and different prediction strategies.
  - Run LLMs via Ollama (Docker-internal, local, or container-based local backends).

- **Built-in Assistant**
  - Use the integrated AI assistant to help with navigation and getting things done faster inside the platform.
  - Configure the assistant’s model and Ollama source in **Settings** (local vs. container).

> **Note:** Some Functions may require an **Alpha Vantage API key** set in **Settings → Global Settings** (stored only for the current session)."""
    return md