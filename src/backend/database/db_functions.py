from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime, inspect, Date, text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import pandas as pd
import os

def create_av_alchemy_db(folder_name, db_name):
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
    data_folder = os.path.join(project_root, folder_name)
    os.makedirs(data_folder, exist_ok=True)

    db_path = os.path.join(data_folder, f"{db_name}.db")
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base = declarative_base()
    Session = sessionmaker(bind = engine)
    session = Session()

    return engine, Base, session, db_path

engine, Base, session, dbpath = create_av_alchemy_db("data", "alphavantage")
engine_2, Base_2, session_2, dbpath_2 = create_av_alchemy_db("data", "system_config")


from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
Base_2 = declarative_base()

class AV_RAW(Base):
    __tablename__ = "alphavantage_raw_kpi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, index=True)

    # ------------------------------------------------------------------
    # OVERVIEW RAW VALUES (ohne num())
    # ------------------------------------------------------------------
    asset_type = Column(String)
    name = Column(String)
    description = Column(Text)
    cik = Column(String)
    exchange = Column(String)
    currency = Column(String)
    country = Column(String)
    sector = Column(String)
    industry = Column(String)
    address = Column(String)
    official_site = Column(String)
    fiscal_year_end = Column(String)
    latest_quarter = Column(String)

    market_capitalization = Column(String)
    ebitda_overview = Column(String)  # aus overview["EBITDA"]

    pe_ratio = Column(String)
    peg_ratio = Column(String)
    book_value = Column(String)
    dividend_per_share = Column(String)
    dividend_yield_raw = Column(String)  # Rohwert, damit es sich von KPI dividend_yield unterscheidet
    eps = Column(String)
    revenue_per_share_ttm = Column(String)
    profit_margin_raw = Column(String)   # Rohwert, siehe KPI profit_margin unten
    operating_margin_ttm = Column(String)
    return_on_assets_ttm = Column(String)
    return_on_equity_ttm = Column(String)
    revenue_ttm = Column(String)
    gross_profit_ttm = Column(String)
    diluted_eps_ttm = Column(String)

    quarterly_earnings_growth_yoy = Column(String)
    quarterly_revenue_growth_yoy = Column(String)

    analyst_target_price = Column(String)
    analyst_rating_strong_buy = Column(String)
    analyst_rating_buy = Column(String)
    analyst_rating_hold = Column(String)
    analyst_rating_sell = Column(String)
    analyst_rating_strong_sell = Column(String)

    trailing_pe = Column(String)
    forward_pe = Column(String)

    price_to_sales_ratio_ttm = Column(String)
    price_to_book_ratio = Column(String)

    ev_to_revenue = Column(String)
    ev_to_ebitda_raw = Column(String)  # Rohwert, unten gibt es KPI ev_to_ebitda

    beta_raw = Column(String)          # Rohwert, unten gibt es KPI beta

    week_52_high = Column(String)
    week_52_low = Column(String)
    moving_average_50_day = Column(String)
    moving_average_200_day = Column(String)

    shares_outstanding = Column(String)
    shares_float = Column(String)
    percent_insiders = Column(String)
    percent_institutions = Column(String)

    dividend_date = Column(String)
    ex_dividend_date = Column(String)

    # ------------------------------------------------------------------
    # CASHFLOW RAW VALUES (ohne num())
    # ------------------------------------------------------------------
    fiscal_date_ending_cf = Column(String)
    reported_currency_cf = Column(String)

    operating_cashflow_raw = Column(String)
    payments_for_operating_activities = Column(String)
    proceeds_from_operating_activities = Column(String)
    change_in_operating_liabilities = Column(String)
    change_in_operating_assets = Column(String)

    depreciation_depletion_and_amortization = Column(String)
    capital_expenditures_raw = Column(String)
    change_in_receivables = Column(String)
    change_in_inventory = Column(String)
    profit_loss = Column(String)

    cashflow_from_investment = Column(String)
    cashflow_from_financing = Column(String)
    proceeds_from_repayments_of_short_term_debt = Column(String)

    payments_for_repurchase_of_common_stock = Column(String)
    payments_for_repurchase_of_equity = Column(String)
    payments_for_repurchase_of_preferred_stock = Column(String)

    dividend_payout = Column(String)
    dividend_payout_common_stock = Column(String)
    dividend_payout_preferred_stock = Column(String)

    proceeds_from_issuance_of_common_stock = Column(String)
    proceeds_from_issuance_of_long_term_debt_and_capital_securities_net = Column(String)
    proceeds_from_issuance_of_preferred_stock = Column(String)

    proceeds_from_repurchase_of_equity = Column(String)
    proceeds_from_sale_of_treasury_stock = Column(String)

    change_in_cash_and_cash_equivalents = Column(String)
    change_in_exchange_rate = Column(String)

    net_income_cf = Column(String)

    # ------------------------------------------------------------------
    # BALANCE SHEET RAW VALUES (ohne num())
    # ------------------------------------------------------------------
    investments = Column(String)
    inventory_raw = Column(String)
    current_net_receivables = Column(String)
    total_non_current_assets = Column(String)
    property_plant_equipment = Column(String)
    accumulated_depreciation_amortization_ppe = Column(String)
    intangible_assets = Column(String)
    intangible_assets_excluding_goodwill = Column(String)
    goodwill = Column(String)
    long_term_investments = Column(String)
    short_term_investments = Column(String)
    other_current_assets = Column(String)
    other_non_current_assets = Column(String)

    total_liabilities_raw = Column(String)
    total_current_liabilities_raw = Column(String)
    current_accounts_payable = Column(String)
    deferred_revenue = Column(String)
    current_debt = Column(String)
    short_term_debt = Column(String)
    total_non_current_liabilities = Column(String)
    capital_lease_obligations = Column(String)
    long_term_debt = Column(String)
    current_long_term_debt = Column(String)
    long_term_debt_noncurrent = Column(String)
    short_long_term_debt_total = Column(String)
    other_current_liabilities = Column(String)
    other_non_current_liabilities = Column(String)

    total_shareholder_equity_raw = Column(String)
    treasury_stock = Column(String)
    retained_earnings = Column(String)
    common_stock_raw = Column(String)
    common_stock_shares_outstanding = Column(String)

    # ------------------------------------------------------------------
    # INCOME STATEMENT RAW VALUES (ohne num())
    # ------------------------------------------------------------------
    fiscal_date_ending_inc = Column(String)
    reported_currency_inc = Column(String)
    gross_profit_raw = Column(String)
    total_revenue_raw = Column(String)
    cost_of_revenue = Column(String)
    cost_of_goods_and_services_sold = Column(String)
    operating_income_raw = Column(String)
    selling_general_and_administrative = Column(String)
    research_and_development = Column(String)
    operating_expenses = Column(String)
    investment_income_net = Column(String)
    net_interest_income = Column(String)
    interest_income = Column(String)
    interest_expense = Column(String)
    non_interest_income = Column(String)
    other_non_operating_income = Column(String)
    depreciation_raw = Column(String)
    depreciation_and_amortization_raw = Column(String)
    income_before_tax = Column(String)
    income_tax_expense = Column(String)
    interest_and_debt_expense = Column(String)
    net_income_from_continuing_operations = Column(String)
    comprehensive_income_net_of_tax = Column(String)
    ebit = Column(String)
    ebitda_inc = Column(String)  # aus inc["ebitda"]
    net_income_raw = Column(String)

    # ------------------------------------------------------------------
    # VORHANDENE KPI-FELDER (numeric, wie gehabt)
    # ------------------------------------------------------------------
    # price_to_book = Column(Float)              # KBV (direct)
    # dividend_yield = Column(Float)             # Dividendenrendite (direct)
    # payout_ratio = Column(Float)               # Ausschüttungsquote (direct)
    # roe_ttm = Column(Float)                    # ROE (direct)
    # roa_ttm = Column(Float)                    # ROA (direct)
    # profit_margin = Column(Float)              # Nettogewinnmarge (direct)
    # revenue_growth_qoq = Column(Float)         # Umsatzwachstum (direct)
    # earnings_growth_qoq = Column(Float)        # Gewinnwachstum (direct)
    # asset_turnover = Column(Float)             # Kapitalumschlag (direct)
    # equity_ratio = Column(Float)               # Eigenkapitalquote (direct)
    # debt_ratio = Column(Float)                 # Fremdkapitalquote (direct)
    # pe_ratio_kpi = Column(Float)               # KGV (direct)
    # price_to_sales = Column(Float)             # KUV (direct)
    # peg_ratio_kpi = Column(Float)              # PEG Ratio (direct)
    # ev_to_ebitda = Column(Float)               # EV/EBITDA (direct)
    # beta = Column(Float)                       # Beta (direct)
    # eps_kpi = Column(Float)                    # EPS (direct)
    # free_cash_flow = Column(Float)             # Free Cashflow (direct)

    # # ---- Cash Flow (Direct) ----
    # operating_cashflow = Column(Float)         # Operativer Cashflow (direct)
    # capex = Column(Float)                      # CAPEX (direct)

    # # ---- Balance Sheet (Direct) ----
    # total_assets = Column(Float)               # Total Assets (direct)
    # total_liabilities = Column(Float)          # Total Liabilities (direct)
    # total_equity = Column(Float)               # Total Equity (direct)
    # cash = Column(Float)                       # Cash (direct)
    # current_assets = Column(Float)             # Current Assets (direct)
    # current_liabilities = Column(Float)        # Current Liabilities (direct)

    # # ---- Income Statement (Direct) ----
    # revenue = Column(Float)                    # Revenue (direct)
    # gross_profit = Column(Float)               # Gross Profit (direct)
    # operating_income = Column(Float)           # Operating Income (direct)
    # ebitda = Column(Float)                     # EBITDA (direct)
    # net_income = Column(Float)                 # Net Income (direct)

    # # ---- Calculated KPIs ----
    # kcv = Column(Float)                        # Kurs-Cashflow-Verhältnis (calc)
    # roce = Column(Float)                       # ROCE (calc)
    # roic = Column(Float)                       # ROIC (calc)
    # gross_margin = Column(Float)               # Bruttogewinnmarge (calc)
    # ebit_margin = Column(Float)                # EBIT-Marge (calc)
    # ebitda_margin = Column(Float)              # EBITDA-Marge (calc)
    # working_capital = Column(Float)            # Working Capital (calc)
    # cashflow_margin = Column(Float)            # Cashflow-Marge (calc)
    # cash_ratio = Column(Float)                 # Liquidität 1. Grades (calc)
    # quick_ratio = Column(Float)                # Liquidität 2. Grades (calc)
    # current_ratio = Column(Float)              # Liquidität 3. Grades (calc)
    # leverage_ratio = Column(Float)             # Verschuldungsgrad (calc)
    # graham_number = Column(Float)              # Graham-Number (calc)

    # # ---- NOT AVAILABLE KPIs ----
    # dyn_verschuldungsgrad = Column(Float)      # Dynamischer Verschuldungsgrad (na)
    # zinsdeckungsgrad = Column(Float)           # Zinsdeckungsgrad (na)
    # anlagendeckungsgrad_1 = Column(Float)      # Anlagendeckungsgrad I (na)
    # anlagendeckungsgrad_2 = Column(Float)      # Anlagendeckungsgrad II (na)

    # ---- Metadata ----
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class System_Config(Base_2):
    __tablename__ = "global_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Value = Column(String)
    Tag = Column(Boolean, nullable=False)



class AV_PRICING(Base):
    __tablename__ = "alphavantage_daily_pricing"

    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Symbol
    symbol = Column(String, index=True, nullable=False)

    # Datum der Kerze (Primary information)
    date = Column(Date, index=True, nullable=False)

    # Prices
    open = Column(Float)               # 1. open
    high = Column(Float)               # 2. high
    low = Column(Float)                # 3. low
    close = Column(Float)              # 4. close
    adjusted_close = Column(Float)     # 5. adjusted close

    # Volume + Corporate actions
    volume = Column(Float)             # 6. volume
    dividend_amount = Column(Float)    # 7. dividend amount
    split_coefficient = Column(Float)  # 8. split coefficient

    # Timestamp for insert/update
    timestamp = Column(DateTime(timezone=True), server_default=func.now())




# -------------------------------------------------
# Prüfen, ob die Tabelle existiert → falls nicht, erstellen
# -------------------------------------------------
inspector = inspect(engine)
inspector_cfg = inspect(engine_2)

if "alphavantage_raw_kpi" not in inspector.get_table_names():
    Base.metadata.create_all(engine)
    print("✔ Tabelle erstellt.")
else:
    print("✔ Tabelle existiert bereits – kein Erstellen nötig.")

if "alphavantage_daily_pricing" not in inspector.get_table_names():
    Base.metadata.create_all(engine)
    print("✔ Tabelle erstellt.")
else:
    print("✔ Tabelle existiert bereits – kein Erstellen nötig.")

if "assistant_config" not in inspector_cfg.get_table_names():
    Base_2.metadata.create_all(engine_2)
    print("✔ Tabelle erstellt.")
else:
    print("✔ Tabelle existiert bereits – kein Erstellen nötig.")


# -------------------------------------------------
# Funktion zum Erstellen eines neuen Eintrags
# -------------------------------------------------
def create_av_raw_entry(
    symbol: str,

    # ------------------------------------------------------------------
    # OVERVIEW RAW VALUES
    # ------------------------------------------------------------------
    asset_type=None,
    name=None,
    description=None,
    cik=None,
    exchange=None,
    currency=None,
    country=None,
    sector=None,
    industry=None,
    address=None,
    official_site=None,
    fiscal_year_end=None,
    latest_quarter=None,

    market_capitalization=None,
    ebitda_overview=None,

    pe_ratio=None,
    peg_ratio=None,
    book_value=None,
    dividend_per_share=None,
    dividend_yield_raw=None,
    eps=None,
    revenue_per_share_ttm=None,
    profit_margin_raw=None,
    operating_margin_ttm=None,
    return_on_assets_ttm=None,
    return_on_equity_ttm=None,
    revenue_ttm=None,
    gross_profit_ttm=None,
    diluted_eps_ttm=None,

    quarterly_earnings_growth_yoy=None,
    quarterly_revenue_growth_yoy=None,

    analyst_target_price=None,
    analyst_rating_strong_buy=None,
    analyst_rating_buy=None,
    analyst_rating_hold=None,
    analyst_rating_sell=None,
    analyst_rating_strong_sell=None,

    trailing_pe=None,
    forward_pe=None,

    price_to_sales_ratio_ttm=None,
    price_to_book_ratio=None,

    ev_to_revenue=None,
    ev_to_ebitda_raw=None,

    beta_raw=None,

    week_52_high=None,
    week_52_low=None,
    moving_average_50_day=None,
    moving_average_200_day=None,

    shares_outstanding=None,
    shares_float=None,
    percent_insiders=None,
    percent_institutions=None,

    dividend_date=None,
    ex_dividend_date=None,

    # ------------------------------------------------------------------
    # CASHFLOW RAW VALUES
    # ------------------------------------------------------------------
    fiscal_date_ending_cf=None,
    reported_currency_cf=None,

    operating_cashflow_raw=None,
    payments_for_operating_activities=None,
    proceeds_from_operating_activities=None,
    change_in_operating_liabilities=None,
    change_in_operating_assets=None,

    depreciation_depletion_and_amortization=None,
    capital_expenditures_raw=None,
    change_in_receivables=None,
    change_in_inventory=None,
    profit_loss=None,

    cashflow_from_investment=None,
    cashflow_from_financing=None,
    proceeds_from_repayments_of_short_term_debt=None,

    payments_for_repurchase_of_common_stock=None,
    payments_for_repurchase_of_equity=None,
    payments_for_repurchase_of_preferred_stock=None,

    dividend_payout=None,
    dividend_payout_common_stock=None,
    dividend_payout_preferred_stock=None,

    proceeds_from_issuance_of_common_stock=None,
    proceeds_from_issuance_of_long_term_debt_and_capital_securities_net=None,
    proceeds_from_issuance_of_preferred_stock=None,

    proceeds_from_repurchase_of_equity=None,
    proceeds_from_sale_of_treasury_stock=None,

    change_in_cash_and_cash_equivalents=None,
    change_in_exchange_rate=None,

    net_income_cf=None,

    # ------------------------------------------------------------------
    # BALANCE SHEET RAW VALUES
    # ------------------------------------------------------------------
    investments=None,
    inventory_raw=None,
    current_net_receivables=None,
    total_non_current_assets=None,
    property_plant_equipment=None,
    accumulated_depreciation_amortization_ppe=None,
    intangible_assets=None,
    intangible_assets_excluding_goodwill=None,
    goodwill=None,
    long_term_investments=None,
    short_term_investments=None,
    other_current_assets=None,
    other_non_current_assets=None,

    total_liabilities_raw=None,
    total_current_liabilities_raw=None,
    current_accounts_payable=None,
    deferred_revenue=None,
    current_debt=None,
    short_term_debt=None,
    total_non_current_liabilities=None,
    capital_lease_obligations=None,
    long_term_debt=None,
    current_long_term_debt=None,
    long_term_debt_noncurrent=None,
    short_long_term_debt_total=None,
    other_current_liabilities=None,
    other_non_current_liabilities=None,

    total_shareholder_equity_raw=None,
    treasury_stock=None,
    retained_earnings=None,
    common_stock_raw=None,
    common_stock_shares_outstanding=None,

    # ------------------------------------------------------------------
    # INCOME STATEMENT RAW VALUES
    # ------------------------------------------------------------------
    fiscal_date_ending_inc=None,
    reported_currency_inc=None,
    gross_profit_raw=None,
    total_revenue_raw=None,
    cost_of_revenue=None,
    cost_of_goods_and_services_sold=None,
    operating_income_raw=None,
    selling_general_and_administrative=None,
    research_and_development=None,
    operating_expenses=None,
    investment_income_net=None,
    net_interest_income=None,
    interest_income=None,
    interest_expense=None,
    non_interest_income=None,
    other_non_operating_income=None,
    depreciation_raw=None,
    depreciation_and_amortization_raw=None,
    income_before_tax=None,
    income_tax_expense=None,
    interest_and_debt_expense=None,
    net_income_from_continuing_operations=None,
    comprehensive_income_net_of_tax=None,
    ebit=None,
    ebitda_inc=None,
    net_income_raw=None,

):
    """Erstellt einen vollständigen AlphaVantage-DB-Eintrag (Rohdaten + KPIs)."""

    entry = AV_RAW(
        symbol=symbol,

        # --- Overview raw ---
        asset_type=asset_type,
        name=name,
        description=description,
        cik=cik,
        exchange=exchange,
        currency=currency,
        country=country,
        sector=sector,
        industry=industry,
        address=address,
        official_site=official_site,
        fiscal_year_end=fiscal_year_end,
        latest_quarter=latest_quarter,

        market_capitalization=market_capitalization,
        ebitda_overview=ebitda_overview,

        pe_ratio=pe_ratio,
        peg_ratio=peg_ratio,
        book_value=book_value,
        dividend_per_share=dividend_per_share,
        dividend_yield_raw=dividend_yield_raw,
        eps=eps,
        revenue_per_share_ttm=revenue_per_share_ttm,
        profit_margin_raw=profit_margin_raw,
        operating_margin_ttm=operating_margin_ttm,
        return_on_assets_ttm=return_on_assets_ttm,
        return_on_equity_ttm=return_on_equity_ttm,
        revenue_ttm=revenue_ttm,
        gross_profit_ttm=gross_profit_ttm,
        diluted_eps_ttm=diluted_eps_ttm,

        quarterly_earnings_growth_yoy=quarterly_earnings_growth_yoy,
        quarterly_revenue_growth_yoy=quarterly_revenue_growth_yoy,

        analyst_target_price=analyst_target_price,
        analyst_rating_strong_buy=analyst_rating_strong_buy,
        analyst_rating_buy=analyst_rating_buy,
        analyst_rating_hold=analyst_rating_hold,
        analyst_rating_sell=analyst_rating_sell,
        analyst_rating_strong_sell=analyst_rating_strong_sell,

        trailing_pe=trailing_pe,
        forward_pe=forward_pe,

        price_to_sales_ratio_ttm=price_to_sales_ratio_ttm,
        price_to_book_ratio=price_to_book_ratio,

        ev_to_revenue=ev_to_revenue,
        ev_to_ebitda_raw=ev_to_ebitda_raw,

        beta_raw=beta_raw,

        week_52_high=week_52_high,
        week_52_low=week_52_low,
        moving_average_50_day=moving_average_50_day,
        moving_average_200_day=moving_average_200_day,

        shares_outstanding=shares_outstanding,
        shares_float=shares_float,
        percent_insiders=percent_insiders,
        percent_institutions=percent_institutions,

        dividend_date=dividend_date,
        ex_dividend_date=ex_dividend_date,

        # --- Cashflow raw ---
        fiscal_date_ending_cf=fiscal_date_ending_cf,
        reported_currency_cf=reported_currency_cf,

        operating_cashflow_raw=operating_cashflow_raw,
        payments_for_operating_activities=payments_for_operating_activities,
        proceeds_from_operating_activities=proceeds_from_operating_activities,
        change_in_operating_liabilities=change_in_operating_liabilities,
        change_in_operating_assets=change_in_operating_assets,

        depreciation_depletion_and_amortization=depreciation_depletion_and_amortization,
        capital_expenditures_raw=capital_expenditures_raw,
        change_in_receivables=change_in_receivables,
        change_in_inventory=change_in_inventory,
        profit_loss=profit_loss,

        cashflow_from_investment=cashflow_from_investment,
        cashflow_from_financing=cashflow_from_financing,
        proceeds_from_repayments_of_short_term_debt=proceeds_from_repayments_of_short_term_debt,

        payments_for_repurchase_of_common_stock=payments_for_repurchase_of_common_stock,
        payments_for_repurchase_of_equity=payments_for_repurchase_of_equity,
        payments_for_repurchase_of_preferred_stock=payments_for_repurchase_of_preferred_stock,

        dividend_payout=dividend_payout,
        dividend_payout_common_stock=dividend_payout_common_stock,
        dividend_payout_preferred_stock=dividend_payout_preferred_stock,

        proceeds_from_issuance_of_common_stock=proceeds_from_issuance_of_common_stock,
        proceeds_from_issuance_of_long_term_debt_and_capital_securities_net=(
            proceeds_from_issuance_of_long_term_debt_and_capital_securities_net
        ),
        proceeds_from_issuance_of_preferred_stock=proceeds_from_issuance_of_preferred_stock,

        proceeds_from_repurchase_of_equity=proceeds_from_repurchase_of_equity,
        proceeds_from_sale_of_treasury_stock=proceeds_from_sale_of_treasury_stock,

        change_in_cash_and_cash_equivalents=change_in_cash_and_cash_equivalents,
        change_in_exchange_rate=change_in_exchange_rate,

        net_income_cf=net_income_cf,

        # --- Balance sheet raw ---
        investments=investments,
        inventory_raw=inventory_raw,
        current_net_receivables=current_net_receivables,
        total_non_current_assets=total_non_current_assets,
        property_plant_equipment=property_plant_equipment,
        accumulated_depreciation_amortization_ppe=accumulated_depreciation_amortization_ppe,
        intangible_assets=intangible_assets,
        intangible_assets_excluding_goodwill=intangible_assets_excluding_goodwill,
        goodwill=goodwill,
        long_term_investments=long_term_investments,
        short_term_investments=short_term_investments,
        other_current_assets=other_current_assets,
        other_non_current_assets=other_non_current_assets,

        total_liabilities_raw=total_liabilities_raw,
        total_current_liabilities_raw=total_current_liabilities_raw,
        current_accounts_payable=current_accounts_payable,
        deferred_revenue=deferred_revenue,
        current_debt=current_debt,
        short_term_debt=short_term_debt,
        total_non_current_liabilities=total_non_current_liabilities,
        capital_lease_obligations=capital_lease_obligations,
        long_term_debt=long_term_debt,
        current_long_term_debt=current_long_term_debt,
        long_term_debt_noncurrent=long_term_debt_noncurrent,
        short_long_term_debt_total=short_long_term_debt_total,
        other_current_liabilities=other_current_liabilities,
        other_non_current_liabilities=other_non_current_liabilities,

        total_shareholder_equity_raw=total_shareholder_equity_raw,
        treasury_stock=treasury_stock,
        retained_earnings=retained_earnings,
        common_stock_raw=common_stock_raw,
        common_stock_shares_outstanding=common_stock_shares_outstanding,

        # --- Income statement raw ---
        fiscal_date_ending_inc=fiscal_date_ending_inc,
        reported_currency_inc=reported_currency_inc,
        gross_profit_raw=gross_profit_raw,
        total_revenue_raw=total_revenue_raw,
        cost_of_revenue=cost_of_revenue,
        cost_of_goods_and_services_sold=cost_of_goods_and_services_sold,
        operating_income_raw=operating_income_raw,
        selling_general_and_administrative=selling_general_and_administrative,
        research_and_development=research_and_development,
        operating_expenses=operating_expenses,
        investment_income_net=investment_income_net,
        net_interest_income=net_interest_income,
        interest_income=interest_income,
        interest_expense=interest_expense,
        non_interest_income=non_interest_income,
        other_non_operating_income=other_non_operating_income,
        depreciation_raw=depreciation_raw,
        depreciation_and_amortization_raw=depreciation_and_amortization_raw,
        income_before_tax=income_before_tax,
        income_tax_expense=income_tax_expense,
        interest_and_debt_expense=interest_and_debt_expense,
        net_income_from_continuing_operations=net_income_from_continuing_operations,
        comprehensive_income_net_of_tax=comprehensive_income_net_of_tax,
        ebit=ebit,
        ebitda_inc=ebitda_inc,
        net_income_raw=net_income_raw,

    )

    try:
        session.add(entry)
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"ERROR beim Speichern von {symbol}")

    print(f"✔ Rohdaten + KPIs für {symbol} gespeichert.")
    return entry

   
def create_av_pricing_entry(
    symbol: str,
    date,  # kann str "YYYY-MM-DD" oder datetime.date sein

    open: float = None,
    high: float = None,
    low: float = None,
    close: float = None,
    adjusted_close: float = None,

    volume: float = None,
    dividend_amount: float = None,
    split_coefficient: float = None,
):
    """
    Erzeugt einen AV_PRICING-Eintrag für TIME_SERIES_DAILY_ADJUSTED.
    """

    # Datum in datetime.date umwandeln, falls als String übergeben
    if isinstance(date, str):
        # AlphaVantage liefert Datum als "YYYY-MM-DD"
        date = datetime.strptime(date, "%Y-%m-%d").date()

    entry = AV_PRICING(
        symbol=symbol,
        date=date,

        open=open,
        high=high,
        low=low,
        close=close,
        adjusted_close=adjusted_close,

        volume=volume,
        dividend_amount=dividend_amount,
        split_coefficient=split_coefficient,
    )

    try:
        session.add(entry)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"ERROR beim Speichern von Pricing für {symbol} am {date}: {e}")
        return None

    print(f"✔ Pricing-Daten für {symbol} am {date} gespeichert.")
    return entry


def get_table(table_name: str):
    """
    Lädt eine SQLAlchemy-Tabelle per Name als DataFrame.
    Nutzt automatisch die globale engine aus deiner DB-Struktur.
    """
    inspector = inspect(engine)
    
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Tabelle '{table_name}' existiert nicht in der Datenbank.")

    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except:
        return f"{table_name} not found!"

def get_table_names(database_path: str):
    """
    Gibt eine Liste aller Tabellen in einer SQLite-Datenbank zurück.
    """
    engine = create_engine(f"sqlite:///{database_path}")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    df = pd.DataFrame({"table_name": tables})
    return df

def delete_table(database_path: str, table_name: str):
    """
    Löscht eine Tabelle in der SQLite-Datenbank.
    """
    engine = create_engine(f"sqlite:///{database_path}")

    with engine.connect() as conn:
        conn.execute(text(f"DELETE FROM {table_name}"))
        conn.commit()

    return f"Table '{table_name}' deleted."

from sqlalchemy.orm import Session

def add_system_config(name: str, value: str = None, tag: bool = False):
    new_entry = System_Config(
        Name=name,
        Value=value,
        Tag=tag
    )
    session_2.add(new_entry)
    session_2.commit()
    session_2.refresh(new_entry)
    return new_entry

def get_system_config_by_name(name: str):
    return session_2.query(System_Config).filter(System_Config.Name == name).first()

def get_config_dict(name: str):
    entry = get_system_config_by_name(name)
    if not entry:
        return None
    return {
        "id": entry.id,
        "Name": entry.Name,
        "Value": entry.Value,
        "Tag": entry.Tag
    }