import os
from dotenv import load_dotenv
import requests
import json
from ..data_model import initial_tickers
import time
import streamlit as st
from ..database.db_functions import create_av_raw_entry, create_av_pricing_entry
load_dotenv()


BASE_URL = "https://www.alphavantage.co/query"
API_KEY = st.session_state.get("alphavantage_key")





# Wie lange VOR jedem Request gewartet wird (in Sekunden)
ALPHAVANTAGE_BASE_SLEEP = 20  # z.B. 20 Sekunden

# Wie lange gewartet wird, wenn ein "Note" (Rate Limit) kommt
ALPHAVANTAGE_LIMIT_SLEEP = 75  # z.B. 75 Sekunden

symbol = initial_tickers[0]

def av_request(params, sleep_before: float = ALPHAVANTAGE_BASE_SLEEP):
    """Hilfsfunktion: API-Aufruf mit bewusst langer Wartezeit."""
    API_KEY = st.session_state.get("alpha_vantage_key")
    params["apikey"] = API_KEY

    

    if not API_KEY:
        st.warning("No Alphavantage Key found!")
        st.stop()

    r = requests.get(
        "https://www.alphavantage.co/query",
        params={"function": "GLOBAL_QUOTE", "symbol": "IBM", "apikey": API_KEY},
        timeout=10,
    )

    if r.status_code != 200:
        st.error(f"HTTP error: {r.status_code}")
        st.stop()

    data_key = r.json()

    # AlphaVantage-Fehlerfälle trotz HTTP 200:
    if "Error Message" in data_key or "Information" in data_key or "Note" in data_key:
        st.error("No valid Alphavantage API-Key (or rate limit hit).")
        st.write(data)
        st.stop()

    # Erfolg: "Global Quote" vorhanden?
    if "Global Quote" not in data_key or not data_key["Global Quote"]:
        st.error("Unexpected response from AlphaVantage.")
        st.write(data)
        st.stop()


    # Basis-Wartezeit vor jedem Request
    if sleep_before and sleep_before > 0:
        time.sleep(sleep_before)

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()

        # AlphaVantage Rate-Limit-Hinweis
        if "Note" in data:
            print("⚠ AlphaVantage Limit-Hinweis erhalten:")
            print(data["Note"])
            print(f"⏳ Warte nun {ALPHAVANTAGE_LIMIT_SLEEP} Sekunden und versuche es erneut …")
            time.sleep(ALPHAVANTAGE_LIMIT_SLEEP)
            return av_request(params, sleep_before=0)  # beim Retry nicht nochmal Basis-Sleep

        if "Error Message" in data:
            print("❌ AlphaVantage Fehler: ", data["Error Message"])
            return None

        return data

    except Exception as e:
        print("❌ Request error:", e)
        return None
    
def fetch_alphavantage_raw(symbol: str):
    """Holt alle Rohdaten für einen Ticker von AlphaVantage mit großzügigen Wartezeiten."""
    
    print(f"\n📡 Lade AlphaVantage Rohdaten für {symbol} …")

    # --- Overview ---
    overview = av_request({"function": "OVERVIEW", "symbol": symbol}) or {}

    # --- Cash Flow ---
    cashflow = av_request({"function": "CASH_FLOW", "symbol": symbol}) or {}
    cf = cashflow.get("annualReports", [{}])[0] if "annualReports" in cashflow else {}

    # --- Balance Sheet ---
    balance = av_request({"function": "BALANCE_SHEET", "symbol": symbol}) or {}
    bs = balance.get("annualReports", [{}])[0] if "annualReports" in balance else {}

    # --- Income Statement ---
    income = av_request({"function": "INCOME_STATEMENT", "symbol": symbol}) or {}
    inc = income.get("annualReports", [{}])[0] if "annualReports" in income else {}

    def num(x):
        try:
            return float(x)
        except:
            return None

    entry = create_av_raw_entry(
        symbol=symbol,
        # --- OVERVIEW RAW VALUES (ohne num()) ---
        asset_type = overview.get("AssetType"),
        name = overview.get("Name"),
        description = overview.get("Description"),
        cik = overview.get("CIK"),
        exchange = overview.get("Exchange"),
        currency = overview.get("Currency"),
        country = overview.get("Country"),
        sector = overview.get("Sector"),
        industry = overview.get("Industry"),
        address = overview.get("Address"),
        official_site = overview.get("OfficialSite"),
        fiscal_year_end = overview.get("FiscalYearEnd"),
        latest_quarter = overview.get("LatestQuarter"),

        market_capitalization = overview.get("MarketCapitalization"),
        ebitda_overview = overview.get("EBITDA"),

        pe_ratio = overview.get("PERatio"),
        peg_ratio = overview.get("PEGRatio"),
        book_value = overview.get("BookValue"),
        dividend_per_share = overview.get("DividendPerShare"),
        dividend_yield_raw = overview.get("DividendYield"),
        eps = overview.get("EPS"),
        revenue_per_share_ttm = overview.get("RevenuePerShareTTM"),
        profit_margin_raw = overview.get("ProfitMargin"),
        operating_margin_ttm = overview.get("OperatingMarginTTM"),
        return_on_assets_ttm = overview.get("ReturnOnAssetsTTM"),
        return_on_equity_ttm = overview.get("ReturnOnEquityTTM"),
        revenue_ttm = overview.get("RevenueTTM"),
        gross_profit_ttm = overview.get("GrossProfitTTM"),
        diluted_eps_ttm = overview.get("DilutedEPSTTM"),

        quarterly_earnings_growth_yoy = overview.get("QuarterlyEarningsGrowthYOY"),
        quarterly_revenue_growth_yoy = overview.get("QuarterlyRevenueGrowthYOY"),

        analyst_target_price = overview.get("AnalystTargetPrice"),
        analyst_rating_strong_buy = overview.get("AnalystRatingStrongBuy"),
        analyst_rating_buy = overview.get("AnalystRatingBuy"),
        analyst_rating_hold = overview.get("AnalystRatingHold"),
        analyst_rating_sell = overview.get("AnalystRatingSell"),
        analyst_rating_strong_sell = overview.get("AnalystRatingStrongSell"),

        trailing_pe = overview.get("TrailingPE"),
        forward_pe = overview.get("ForwardPE"),

        price_to_sales_ratio_ttm = overview.get("PriceToSalesRatioTTM"),
        price_to_book_ratio = overview.get("PriceToBookRatio"),

        ev_to_revenue = overview.get("EVToRevenue"),
        ev_to_ebitda_raw = overview.get("EVToEBITDA"),

        beta_raw = overview.get("Beta"),

        week_52_high = overview.get("52WeekHigh"),
        week_52_low = overview.get("52WeekLow"),
        moving_average_50_day = overview.get("50DayMovingAverage"),
        moving_average_200_day = overview.get("200DayMovingAverage"),

        shares_outstanding = overview.get("SharesOutstanding"),
        shares_float = overview.get("SharesFloat"),
        percent_insiders = overview.get("PercentInsiders"),
        percent_institutions = overview.get("PercentInstitutions"),

        dividend_date = overview.get("DividendDate"),
        ex_dividend_date = overview.get("ExDividendDate"),

        # --- CASHFLOW RAW VALUES (ohne num()) ---
        fiscal_date_ending_cf = cf.get("fiscalDateEnding"),
        reported_currency_cf = cf.get("reportedCurrency"),

        operating_cashflow_raw = cf.get("operatingCashflow"),
        payments_for_operating_activities = cf.get("paymentsForOperatingActivities"),
        proceeds_from_operating_activities = cf.get("proceedsFromOperatingActivities"),
        change_in_operating_liabilities = cf.get("changeInOperatingLiabilities"),
        change_in_operating_assets = cf.get("changeInOperatingAssets"),

        depreciation_depletion_and_amortization = cf.get("depreciationDepletionAndAmortization"),
        capital_expenditures_raw = cf.get("capitalExpenditures"),
        change_in_receivables = cf.get("changeInReceivables"),
        change_in_inventory = cf.get("changeInInventory"),
        profit_loss = cf.get("profitLoss"),

        cashflow_from_investment = cf.get("cashflowFromInvestment"),
        cashflow_from_financing = cf.get("cashflowFromFinancing"),
        proceeds_from_repayments_of_short_term_debt = cf.get("proceedsFromRepaymentsOfShortTermDebt"),

        payments_for_repurchase_of_common_stock = cf.get("paymentsForRepurchaseOfCommonStock"),
        payments_for_repurchase_of_equity = cf.get("paymentsForRepurchaseOfEquity"),
        payments_for_repurchase_of_preferred_stock = cf.get("paymentsForRepurchaseOfPreferredStock"),

        dividend_payout = cf.get("dividendPayout"),
        dividend_payout_common_stock = cf.get("dividendPayoutCommonStock"),
        dividend_payout_preferred_stock = cf.get("dividendPayoutPreferredStock"),

        proceeds_from_issuance_of_common_stock = cf.get("proceedsFromIssuanceOfCommonStock"),
        proceeds_from_issuance_of_long_term_debt_and_capital_securities_net =
            cf.get("proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"),
        proceeds_from_issuance_of_preferred_stock = cf.get("proceedsFromIssuanceOfPreferredStock"),

        proceeds_from_repurchase_of_equity = cf.get("proceedsFromRepurchaseOfEquity"),
        proceeds_from_sale_of_treasury_stock = cf.get("proceedsFromSaleOfTreasuryStock"),

        change_in_cash_and_cash_equivalents = cf.get("changeInCashAndCashEquivalents"),
        change_in_exchange_rate = cf.get("changeInExchangeRate"),

        net_income_cf = cf.get("netIncome"),

         # --- BALANCE SHEET RAW VALUES (ohne num()) ---
        investments = bs.get("investments"),
        inventory_raw = bs.get("inventory"),
        current_net_receivables = bs.get("currentNetReceivables"),
        total_non_current_assets = bs.get("totalNonCurrentAssets"),
        property_plant_equipment = bs.get("propertyPlantEquipment"),
        accumulated_depreciation_amortization_ppe = bs.get("accumulatedDepreciationAmortizationPPE"),
        intangible_assets = bs.get("intangibleAssets"),
        intangible_assets_excluding_goodwill = bs.get("intangibleAssetsExcludingGoodwill"),
        goodwill = bs.get("goodwill"),
        long_term_investments = bs.get("longTermInvestments"),
        short_term_investments = bs.get("shortTermInvestments"),
        other_current_assets = bs.get("otherCurrentAssets"),
        other_non_current_assets = bs.get("otherNonCurrentAssets"),

        total_liabilities_raw = bs.get("totalLiabilities"),
        total_current_liabilities_raw = bs.get("totalCurrentLiabilities"),
        current_accounts_payable = bs.get("currentAccountsPayable"),
        deferred_revenue = bs.get("deferredRevenue"),
        current_debt = bs.get("currentDebt"),
        short_term_debt = bs.get("shortTermDebt"),
        total_non_current_liabilities = bs.get("totalNonCurrentLiabilities"),
        capital_lease_obligations = bs.get("capitalLeaseObligations"),
        long_term_debt = bs.get("longTermDebt"),
        current_long_term_debt = bs.get("currentLongTermDebt"),
        long_term_debt_noncurrent = bs.get("longTermDebtNoncurrent"),
        short_long_term_debt_total = bs.get("shortLongTermDebtTotal"),
        other_current_liabilities = bs.get("otherCurrentLiabilities"),
        other_non_current_liabilities = bs.get("otherNonCurrentLiabilities"),

        total_shareholder_equity_raw = bs.get("totalShareholderEquity"),
        treasury_stock = bs.get("treasuryStock"),
        retained_earnings = bs.get("retainedEarnings"),
        common_stock_raw = bs.get("commonStock"),
        common_stock_shares_outstanding = bs.get("commonStockSharesOutstanding"),

        # --- INCOME STATEMENT RAW VALUES (ohne num()) ---
        fiscal_date_ending_inc = inc.get("fiscalDateEnding"),
        reported_currency_inc = inc.get("reportedCurrency"),
        gross_profit_raw = inc.get("grossProfit"),
        total_revenue_raw = inc.get("totalRevenue"),
        cost_of_revenue = inc.get("costOfRevenue"),
        cost_of_goods_and_services_sold = inc.get("costofGoodsAndServicesSold"),
        operating_income_raw = inc.get("operatingIncome"),
        selling_general_and_administrative = inc.get("sellingGeneralAndAdministrative"),
        research_and_development = inc.get("researchAndDevelopment"),
        operating_expenses = inc.get("operatingExpenses"),
        investment_income_net = inc.get("investmentIncomeNet"),
        net_interest_income = inc.get("netInterestIncome"),
        interest_income = inc.get("interestIncome"),
        interest_expense = inc.get("interestExpense"),
        non_interest_income = inc.get("nonInterestIncome"),
        other_non_operating_income = inc.get("otherNonOperatingIncome"),
        depreciation_raw = inc.get("depreciation"),
        depreciation_and_amortization_raw = inc.get("depreciationAndAmortization"),
        income_before_tax = inc.get("incomeBeforeTax"),
        income_tax_expense = inc.get("incomeTaxExpense"),
        interest_and_debt_expense = inc.get("interestAndDebtExpense"),
        net_income_from_continuing_operations = inc.get("netIncomeFromContinuingOperations"),
        comprehensive_income_net_of_tax = inc.get("comprehensiveIncomeNetOfTax"),
        ebit = inc.get("ebit"),
        ebitda_inc = inc.get("ebitda"),
        net_income_raw = inc.get("netIncome"),
       
    )

    print(f"✔ Rohdaten für {symbol} gespeichert.")
    return entry

def fetch_alphavantage_price_today(symbol: str):
    """Holt nur den neuesten Tagespreis für einen Ticker und speichert ihn in AV_PRICING."""

    print(f"\n📡 Lade heutigen Preis für {symbol} …")

    data = av_request({
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact"
    }) or {}

    ts = data.get("Time Series (Daily)", {})

    if not ts:
        print(f"❌ Keine Tagespreise für {symbol} erhalten!")
        return None

    # Neuester Eintrag ist das erste Element
    latest_date = sorted(ts.keys(), reverse=True)[0]
    values = ts[latest_date]

    entry = create_av_pricing_entry(
        symbol=symbol,
        date=latest_date,

        open=values.get("1. open"),
        high=values.get("2. high"),
        low=values.get("3. low"),
        close=values.get("4. close"),
        adjusted_close=values.get("5. adjusted close"),

        volume=values.get("6. volume"),
        dividend_amount=values.get("7. dividend amount"),
        split_coefficient=values.get("8. split coefficient"),
    )

    print(f"✔ Price for {symbol} saved: {latest_date}")
    return entry