kpi_list = [
    "Kurs-Buchwert-Verhältnis (KBV)",
    "Kurs-Cashflow-Verhältnis (KCV)",
    "Dividendenrendite",
    "Ausschüttungsquote (Payout Ratio)",
    "Eigenkapitalrendite (ROE)",
    "Gesamtkapitalrendite (ROA)",
    "Return on Capital Employed (ROCE)",
    "Return on Invested Capital (ROIC)",
    "Bruttogewinnmarge",
    "EBIT-Marge",
    "EBITDA-Marge",
    "Nettogewinnmarge",
    "Umsatzwachstum",
    "Gewinnwachstum",
    "Kapitalumschlag",
    "Working Capital",
    "Cashflow-Marge",
    "Liquidität 1. Grades (Cash Ratio)",
    "Liquidität 2. Grades (Quick Ratio)",
    "Liquidität 3. Grades (Current Ratio)",
    "Eigenkapitalquote",
    "Fremdkapitalquote",
    "Dynamischer Verschuldungsgrad",
    "Zinsdeckungsgrad",
    "Anlagendeckungsgrad I",
    "Anlagendeckungsgrad II",
    "Kurs-Gewinn-Verhältnis (Wachstum) (KGV)",
    "Kurs-Umsatz-Verhältnis (KUV)",
    "PEG Ratio",
    "Free Cashflow",
    "Operativer Cashflow",
    "Gewinn je Aktie (EPS)",
    "Verschuldungsgrad",
    "EV/EBITDA",
    "Beta",
    "Graham-Number"
]

alpha_vantage_kpis = {
    "Kurs-Buchwert-Verhältnis (KBV)": "PriceToBookRatio",
    "Dividendenrendite": "DividendYield",
    "Ausschüttungsquote (Payout Ratio)": "PayoutRatio",
    "Eigenkapitalrendite (ROE)": "ReturnOnEquityTTM",
    "Gesamtkapitalrendite (ROA)": "ReturnOnAssetsTTM",
    "Nettogewinnmarge": "ProfitMargin",
    "Umsatzwachstum": "QuarterlyRevenueGrowthYOY",  # *4 für annualisiert
    "Gewinnwachstum": "QuarterlyEarningsGrowthYOY",  # *4 für annualisiert
    "Kapitalumschlag": "AssetTurnover",
    "Cashflow-Marge": "operating_cashflow_margin",   # operatingCashFlow / revenue (selbst berechnen)
    "Eigenkapitalquote": "equityRatio",
    "Fremdkapitalquote": "debtRatio",
    "Kurs-Gewinn-Verhältnis (Wachstum) (KGV)": "PERatio",
    "Kurs-Umsatz-Verhältnis (KUV)": "PriceToSalesRatioTTM",
    "PEG Ratio": "PEGRatio",
    "Free Cashflow": "freeCashFlow",                 # operatingCashFlow - capex
    "Operativer Cashflow": "operatingCashFlow",
    "Gewinn je Aktie (EPS)": "EPS",
    "EV/EBITDA": "EVToEBITDA",
    "Beta": "Beta"
}

initial_tickers = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet (Google)
    "AMZN",   # Amazon
    "META",   # Meta Platforms
    "TSLA",   # Tesla
    "NVDA",   # Nvidia
    "JPM",    # JPMorgan Chase
    "V",      # Visa
    "NFLX"    # Netflix
]

TICKERS = [
    # USA – Mega Caps / Tech / Consumer
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA",
    "NFLX", "TSLA", "AMD", "INTC", "QCOM", "ADBE", "CRM", "CSCO",
    "ORCL", "IBM", "PYPL", "SQ", "SHOP", "UBER",

    # USA – Consumer & Retail
    "WMT", "HD", "LOW", "COST", "TGT", "DIS", "MCD", "NKE", "SBUX",

    # USA – Finance
    "JPM", "BAC", "WFC", "C", "GS", "MS", "V", "MA", "AXP",

    # USA – Healthcare
    "JNJ", "PFE", "MRNA", "BMY", "ABBV", "LLY", "GILD", "AMGN",

    # USA – Industrials / Energy
    "XOM", "CVX", "COP", "GE", "CAT", "HON", "LMT",

    # Deutschland – DAX (Top 40)
    "SAP", "SIE", "DTE", "ALV", "BAS", "BAYN", "BMW", "MBG",
    "VOW3", "VNA", "MUV2", "LIN", "HEN3", "DPW", "FRE", "RWE",
    "EOAN", "IFX", "DBK", "HEI",

    # Deutschland – große weitere bekannte Namen
    "ZAL", "PUM", "BEI", "ADS",

    # ETFs – große, liquide, weltweit genutzt
    "SPY", "QQQ", "DIA", "IVV", "VOO",     # USA Index-ETFs
    "IWM",                                 # Russell 2000
    "XLK", "XLF", "XLV", "XLE", "XLI",     # Sektoren
    "XLY", "XLP", "XLB", "XLU",            # weitere Sektoren
    "EEM", "IEMG",                         # Emerging Markets
    "VEA", "VWO",                          # Internationale Märkte
]