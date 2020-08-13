import numpy as np
import pandas as pd
from util import (
    build_base_dataframes,
    build_import_dataframe,
    build_model,
    get_boe_exchange_rates,
    get_ecb_riskfree_rates,
    get_french_data,
)
from v1 import models

pd.options.mode.chained_assignment = None
"""
### ECB Risk Free Rates ###

df_rf_eur_d = get_ecb_riskfree_rates(freq="D")
df_rf_eur_d["currency"] = "EUR"
build_model(model=models.DailyRiskFreeRate, df=df_rf_eur_d)
df_rf_eur_m = get_ecb_riskfree_rates(freq="M")
df_rf_eur_m["currency"] = "EUR"
build_model(model=models.MonthlyRiskFreeRate, df=df_rf_eur_m)
df_rf_eur_a = get_ecb_riskfree_rates(freq="A")
df_rf_eur_a["currency"] = "EUR"
build_model(model=models.AnnuallyRiskFreeRate, df=df_rf_eur_a)

dict_rf_d = {"EUR": df_rf_eur_d}
dict_rf_m = {"EUR": df_rf_eur_m}
dict_rf_a = {"EUR": df_rf_eur_a}

### BOE Exchange Rates USD per X ###

df_fxrates_d = get_boe_exchange_rates(freq="D")
build_model(model=models.DailyExchangeRateUSDPerX, df=df_fxrates_d)
df_fxrates_m = get_boe_exchange_rates(freq="M")
build_model(model=models.MonthlyExchangeRateUSDPerX, df=df_fxrates_m)
df_fxrates_a = get_boe_exchange_rates(freq="A")
build_model(model=models.AnnuallyExchangeRateUSDPerX, df=df_fxrates_a)

df_fxrates_r_d = round((df_fxrates_d / df_fxrates_d.shift(periods=1) - 1), 8)
df_fxrates_r_d.drop(df_fxrates_r_d.index[:1], inplace=True)
df_fxrates_r_m = round((df_fxrates_m / df_fxrates_m.shift(periods=1) - 1), 8)
df_fxrates_r_m.drop(df_fxrates_r_m.index[:1], inplace=True)
df_fxrates_r_a = round((df_fxrates_a / df_fxrates_a.shift(periods=1) - 1), 8)
df_fxrates_r_a.drop(df_fxrates_r_a.index[:1], inplace=True)

### French Factor Returns ###

# USA #

print("Parsing factor returns for USA...")
print("Parsing 3 and 4 factor model returns...", end="")

df_3n4factor_usa_usd_d = get_french_data(
    'F-F_Research_Data_Factors_daily_CSV', 'F-F_Research_Data_Factors_daily.CSV', freq='D')
df_mom_usa_usd_d = get_french_data(
    'F-F_Momentum_Factor_daily_CSV', 'F-F_Momentum_Factor_daily.CSV', freq='D')
df_3n4factor_usa_usd_d, df_rf_usd_d = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_d, df_mom=df_mom_usa_usd_d, region="USA", with_rf=True)
build_model(model=models.DailyRiskFreeRate, df=df_rf_usd_d)
build_model(model=models.DailyThreeFourFactor, df=df_3n4factor_usa_usd_d)

df_3n4factor_usa_usd_m = get_french_data(
    'F-F_Research_Data_Factors_CSV', 'F-F_Research_Data_Factors.CSV', freq='M')
df_mom_usa_usd_m = get_french_data(
    'F-F_Momentum_Factor_CSV', 'F-F_Momentum_Factor.CSV', freq='M')
df_3n4factor_usa_usd_m, df_rf_usd_m = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_m, df_mom=df_mom_usa_usd_m, region="USA", with_rf=True)
build_model(model=models.MonthlyRiskFreeRate, df=df_rf_usd_m)
build_model(model=models.MonthlyThreeFourFactor, df=df_3n4factor_usa_usd_m)

df_3n4factor_usa_usd_a = get_french_data(
    'F-F_Research_Data_Factors_CSV', 'F-F_Research_Data_Factors.CSV', freq='A')
df_mom_usa_usd_a = get_french_data(
    'F-F_Momentum_Factor_CSV', 'F-F_Momentum_Factor.CSV', freq='A')
df_3n4factor_usa_usd_a, df_rf_usd_a = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_a, df_mom=df_mom_usa_usd_a, region="USA", with_rf=True)
build_model(model=models.AnnuallyRiskFreeRate, df=df_rf_usd_a)
build_model(model=models.AnnuallyThreeFourFactor, df=df_3n4factor_usa_usd_a)

print(f"Parsing factor returns for USA... Done.\r")
print("Parsing 5 and 6 factor model returns...", end="")

df_5n6factor_usa_usd_d = get_french_data(
    'F-F_Research_Data_5_Factors_2x3_daily_CSV', 'F-F_Research_Data_5_Factors_2x3_daily.CSV', freq='D')
df_5n6factor_usa_usd_d, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_d, df_mom=df_mom_usa_usd_d, region="USA")
build_model(model=models.DailyFiveSixFactor, df=df_5n6factor_usa_usd_d)

df_5n6factor_usa_usd_m = get_french_data(
    'F-F_Research_Data_5_Factors_2x3_CSV', 'F-F_Research_Data_5_Factors_2x3.CSV', freq='M')
df_5n6factor_usa_usd_m, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_m, df_mom=df_mom_usa_usd_m, region="USA")
build_model(model=models.MonthlyFiveSixFactor, df=df_5n6factor_usa_usd_m)

df_5n6factor_usa_usd_a = get_french_data(
    'F-F_Research_Data_5_Factors_2x3_CSV', 'F-F_Research_Data_5_Factors_2x3.CSV', freq='A')
df_5n6factor_usa_usd_a, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_a, df_mom=df_mom_usa_usd_a, region="USA")
build_model(model=models.AnnuallyFiveSixFactor, df=df_5n6factor_usa_usd_a)

print(f"Parsing 5 and 6 factor model returns... Done.\r")
print("Pushing data to database...", end="")

for currency in df_fxrates_r_d.columns:
    df_target_d = build_import_dataframe(df_factor_source=df_3n4factor_usa_usd_d, df_fxrates_r=df_fxrates_r_d,
                                         df_rf_source=df_rf_usd_d, dict_rf_target=dict_rf_d, region="USA", currency=currency)
    df_target_m = build_import_dataframe(df_factor_source=df_3n4factor_usa_usd_m, df_fxrates_r=df_fxrates_r_m,
                                         df_rf_source=df_rf_usd_m, dict_rf_target=dict_rf_m, region="USA", currency=currency)
    df_target_a = build_import_dataframe(df_factor_source=df_3n4factor_usa_usd_a, df_fxrates_r=df_fxrates_r_a,
                                         df_rf_source=df_rf_usd_a, dict_rf_target=dict_rf_a, region="USA", currency=currency)
    # Create instances
    build_model(model=models.DailyThreeFourFactor, df=df_target_d)
    build_model(model=models.MonthlyThreeFourFactor, df=df_target_m)
    build_model(model=models.AnnuallyThreeFourFactor, df=df_target_a)

print(f"Pushing data to database... Done.\r")
"""

regions = [
    {
        "name": "Developed",
        "freq": [
            {"link": "", "file": "", "model": models.DailyThreeFourFactor},
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
        ],
    },
    {
        "name": "Developed_ex_US",
        "freq": [
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
        ],
    },
    {
        "name": "Europe",
        "freq": [
            {
                "factors": {
                    "link": "Europe_3_Factors_Daily_CSV",
                    "file": "Europe_3_Factors_Daily.csv",
                },
                "mom": {
                    "link": "Europe_MOM_Factor_Daily_CSV",
                    "file": "Europe_MOM_Factor_Daily.csv",
                },
                "model": models.DailyThreeFourFactor,
            },
            {
                "factors": {
                    "link": "Europe_3_Factors_CSV",
                    "file": "Europe_3_Factors.csv",
                },
                "mom": {
                    "link": "Europe_MOM_Factor_CSV",
                    "file": "Europe_MOM_Factor.csv",
                },
                "model": models.MonthlyThreeFourFactor,
            },
            {
                "factors": {
                    "link": "Europe_3_Factors_Daily_CSV",
                    "file": "Europe_3_Factors_Daily.csv",
                },
                "mom": {
                    "link": "Europe_MOM_Factor_Daily_CSV",
                    "file": "Europe_MOM_Factor_Daily.csv",
                },
                "model": models.DailyThreeFourFactor,
            },
        ],
    },
    {
        "name": "Japan",
        "freq": [
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
        ],
    },
    {
        "name": "Asia_Pacific_ex_Japan",
        "freq": [
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
        ],
    },
    {
        "name": "North_America",
        "freq": [
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
            {"link": "", "file": "", "model": ""},
        ],
    },
]

# EUROPE #

df_3n4factor_europe_usd_d = get_french_data(
    "Europe_3_Factors_Daily_CSV", "Europe_3_Factors_Daily.csv", freq="D"
)
df_mom_europe_usd_d = get_french_data(
    "Europe_MOM_Factor_Daily_CSV", "Europe_MOM_Factor_Daily.csv", freq="D"
)
df_3n4factor_europe_usd_d, _ = build_base_dataframes(
    df_factors=df_3n4factor_europe_usd_d,
    df_mom=df_mom_europe_usd_d,
    region="Europe",
    with_rf=False,
)
build_model(model=models.DailyThreeFourFactor, df=df_3n4factor_europe_usd_d)

df_3n4factor_europe_usd_a = get_french_data(
    "Europe_3_Factors_CSV", "Europe_3_Factors.csv", freq="A"
)

df_5factor_europe_usd_d = get_french_data(
    "Europe_5_Factors_Daily_CSV", "Europe_5_Factors_Daily.csv", freq="D"
)
df_5factor_europe_usd_m = get_french_data(
    "Europe_5_Factors_CSV", "Europe_5_Factors.csv", freq="M"
)
df_5factor_europe_usd_a = get_french_data(
    "Europe_5_Factors_CSV", "Europe_5_Factors.csv", freq="A"
)
df_mom_europe_usd_m = get_french_data(
    "Europe_MOM_Factor_CSV", "Europe_MOM_Factor.csv", freq="M"
)
df_mom_europe_usd_a = get_french_data(
    "Europe_MOM_Factor_CSV", "Europe_MOM_Factor.csv", freq="A"
)

df_3n4factor_europe_d = df_3n4factor_europe_usd_d.copy()


build_model(model=models.DailyThreeFourFactor, df=df_3n4factor_usa_d)


# Japan #

df_3factor_japan_d = get_french_data(
    "Japan_3_Factors_Daily_CSV", "Japan_3_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_3factor_japan_m = get_french_data(
    "Japan_3_Factors_CSV", "Japan_3_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_3factor_japan_a = get_french_data(
    "Japan_3_Factors_CSV", "Japan_3_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_5factor_japan_d = get_french_data(
    "Japan_5_Factors_Daily_CSV", "Japan_5_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_5factor_japan_m = get_french_data(
    "Japan_5_Factors_CSV", "Japan_5_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_5factor_japan_a = get_french_data(
    "Japan_5_Factors_CSV", "Japan_5_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_mom_japan_d = get_french_data(
    "Japan_MOM_Factor_Daily_CSV", "Japan_MOM_Factor_Daily.csv", freq="D"
)
df_mom_japan_m = get_french_data(
    "Japan_MOM_Factor_CSV", "Japan_MOM_Factor.csv", freq="M"
)
df_mom_japan_a = get_french_data(
    "Japan_MOM_Factor_CSV", "Japan_MOM_Factor.csv", freq="A"
)

# Developed #

df_3factor_developed_d = get_french_data(
    "Developed_3_Factors_Daily_CSV", "Developed_3_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_3factor_developed_m = get_french_data(
    "Developed_3_Factors_CSV", "Developed_3_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_3factor_developed_a = get_french_data(
    "Developed_3_Factors_CSV", "Developed_3_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_5factor_developed_d = get_french_data(
    "Developed_5_Factors_Daily_CSV", "Developed_5_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_5factor_developed_m = get_french_data(
    "Developed_5_Factors_CSV", "Developed_5_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_5factor_developed_a = get_french_data(
    "Developed_5_Factors_CSV", "Developed_5_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_mom_developed_d = get_french_data(
    "Developed_MOM_Factor_Daily_CSV", "Developed_MOM_Factor_Daily.csv", freq="D"
)
df_mom_developed_m = get_french_data(
    "Developed_MOM_Factor_CSV", "Developed_MOM_Factor.csv", freq="M"
)
df_mom_developed_a = get_french_data(
    "Developed_MOM_Factor_CSV", "Developed_MOM_Factor.csv", freq="A"
)

# Developed_ex_US #

df_3factor_developed_ex_US_d = get_french_data(
    "Developed_ex_US_3_Factors_Daily_CSV",
    "Developed_ex_US_3_Factors_Daily.csv",
    freq="D",
).drop(["RF"], axis=1)
df_3factor_developed_ex_US_m = get_french_data(
    "Developed_ex_US_3_Factors_CSV", "Developed_ex_US_3_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_3factor_developed_ex_US_a = get_french_data(
    "Developed_ex_US_3_Factors_CSV", "Developed_ex_US_3_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_5factor_developed_ex_US_d = get_french_data(
    "Developed_ex_US_5_Factors_Daily_CSV",
    "Developed_ex_US_5_Factors_Daily.csv",
    freq="D",
).drop(["RF"], axis=1)
df_5factor_developed_ex_US_m = get_french_data(
    "Developed_ex_US_5_Factors_CSV", "Developed_ex_US_5_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_5factor_developed_ex_US_a = get_french_data(
    "Developed_ex_US_5_Factors_CSV", "Developed_ex_US_5_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_mom_developed_ex_US_d = get_french_data(
    "Developed_ex_US_MOM_Factor_Daily_CSV",
    "Developed_ex_US_MOM_Factor_Daily.csv",
    freq="D",
)
df_mom_developed_ex_US_m = get_french_data(
    "Developed_ex_US_MOM_Factor_CSV", "Developed_ex_US_MOM_Factor.csv", freq="M"
)
df_mom_developed_ex_US_a = get_french_data(
    "Developed_ex_US_MOM_Factor_CSV", "Developed_ex_US_MOM_Factor.csv", freq="A"
)

# Asia_Pacific_ex_Japan #

df_3factor_Asia_Pacific_ex_Japan_d = get_french_data(
    "Asia_Pacific_ex_Japan_3_Factors_Daily_CSV",
    "Asia_Pacific_ex_Japan_3_Factors_Daily.csv",
    freq="D",
).drop(["RF"], axis=1)
df_3factor_Asia_Pacific_ex_Japan_m = get_french_data(
    "Asia_Pacific_ex_Japan_3_Factors_CSV",
    "Asia_Pacific_ex_Japan_3_Factors.csv",
    freq="M",
).drop(["RF"], axis=1)
df_3factor_Asia_Pacific_ex_Japan_a = get_french_data(
    "Asia_Pacific_ex_Japan_3_Factors_CSV",
    "Asia_Pacific_ex_Japan_3_Factors.csv",
    freq="A",
).drop(["RF"], axis=1)
df_5factor_Asia_Pacific_ex_Japan_d = get_french_data(
    "Asia_Pacific_ex_Japan_5_Factors_Daily_CSV",
    "Asia_Pacific_ex_Japan_5_Factors_Daily.csv",
    freq="D",
).drop(["RF"], axis=1)
df_5factor_Asia_Pacific_ex_Japan_m = get_french_data(
    "Asia_Pacific_ex_Japan_5_Factors_CSV",
    "Asia_Pacific_ex_Japan_5_Factors.csv",
    freq="M",
).drop(["RF"], axis=1)
df_5factor_Asia_Pacific_ex_Japan_a = get_french_data(
    "Asia_Pacific_ex_Japan_5_Factors_CSV",
    "Asia_Pacific_ex_Japan_5_Factors.csv",
    freq="A",
).drop(["RF"], axis=1)
df_mom_Asia_Pacific_ex_Japan_d = get_french_data(
    "Asia_Pacific_ex_Japan_MOM_Factor_Daily_CSV",
    "Asia_Pacific_ex_Japan_MOM_Factor_Daily.csv",
    freq="D",
)
df_mom_Asia_Pacific_ex_Japan_m = get_french_data(
    "Asia_Pacific_ex_Japan_MOM_Factor_CSV",
    "Asia_Pacific_ex_Japan_MOM_Factor.csv",
    freq="M",
)
df_mom_Asia_Pacific_ex_Japan_a = get_french_data(
    "Asia_Pacific_ex_Japan_MOM_Factor_CSV",
    "Asia_Pacific_ex_Japan_MOM_Factor.csv",
    freq="A",
)

# North_America #

df_3factor_north_america_d = get_french_data(
    "North_America_3_Factors_Daily_CSV", "North_America_3_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_3factor_north_america_m = get_french_data(
    "North_America_3_Factors_CSV", "North_America_3_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_3factor_north_america_a = get_french_data(
    "North_America_3_Factors_CSV", "North_America_3_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_5factor_north_america_d = get_french_data(
    "North_America_5_Factors_Daily_CSV", "North_America_5_Factors_Daily.csv", freq="D"
).drop(["RF"], axis=1)
df_5factor_north_america_m = get_french_data(
    "North_America_5_Factors_CSV", "North_America_5_Factors.csv", freq="M"
).drop(["RF"], axis=1)
df_5factor_north_america_a = get_french_data(
    "North_America_5_Factors_CSV", "North_America_5_Factors.csv", freq="A"
).drop(["RF"], axis=1)
df_mom_north_america_d = get_french_data(
    "North_America_MOM_Factor_Daily_CSV", "North_America_MOM_Factor_Daily.csv", freq="D"
)
df_mom_north_america_m = get_french_data(
    "North_America_MOM_Factor_CSV", "North_America_MOM_Factor.csv", freq="M"
)
df_mom_north_america_a = get_french_data(
    "North_America_MOM_Factor_CSV", "North_America_MOM_Factor.csv", freq="A"
)


print("Finished data import successfully!")
