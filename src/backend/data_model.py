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

tickers = [
     "AAPL",   # Apple
 #   "MSFT",   # Microsoft
 #   "GOOGL",  # Alphabet (Google)
 #   "AMZN",   # Amazon
 #   "META",   # Meta Platforms
 #   "TSLA",   # Tesla
 #   "NVDA",   # Nvidia
 #   "JPM",    # JPMorgan Chase
 #   "V",      # Visa
 #   "NFLX"    # Netflix
]