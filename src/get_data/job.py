import pandas as pd

from beta import models
from get_data.config.french import regions
from get_data.config.general import currencies_fxrates
from get_data.convert import FactorConverter
from get_data.fetch import Fetcher as fe

pd.options.mode.chained_assignment = None

print("Starting data import of factor returns, riskfree rates and exchange rates...")

# ECB Risk Free Rates #
df_rf_eur_d = fe.ecb_riskfreerates("daily")
df_rf_eur_m = fe.ecb_riskfreerates("monthly")
df_rf_eur_a = fe.ecb_riskfreerates("annual")

models.RiskFreeRate.from_dataframe(df_rf_eur_d, "daily", "EUR")
models.RiskFreeRate.from_dataframe(df_rf_eur_m, "monthly", "EUR")
models.RiskFreeRate.from_dataframe(df_rf_eur_a, "annual", "EUR")

# Possibly add riskfree rates for other currencies here
dict_rf_d = {"EUR": df_rf_eur_d}
dict_rf_m = {"EUR": df_rf_eur_m}
dict_rf_a = {"EUR": df_rf_eur_a}

# BOE Exchange Rates USD per X #

df_fxrates_d = fe.boe_fxrates("daily")
df_fxrates_m = fe.boe_fxrates("monthly")
df_fxrates_a = fe.boe_fxrates("annual")

models.ExchangeRateUSDPerX.from_dataframe(df_fxrates_d, "daily")
models.ExchangeRateUSDPerX.from_dataframe(df_fxrates_m, "monthly")
models.ExchangeRateUSDPerX.from_dataframe(df_fxrates_a, "annual")

# French Factor Returns #

# USA #

print("Parsing factor returns for USA...")

df_3n4factor_usa_usd_d = fe.french_factors("F-F_Research_Data_Factors_daily_CSV", "daily")
df_mom_usa_usd_d = fe.french_factors("F-F_Momentum_Factor_daily_CSV", "daily")

df_rf_usd_d = df_3n4factor_usa_usd_d[["rf"]]
df_3n4factor_usa_usd_d.drop(["rf"], axis=1, inplace=True)
df_3n4factor_usa_usd_d["mom"] = df_mom_usa_usd_d["mom"]

models.ThreeFourFactor.from_dataframe(df_3n4factor_usa_usd_d, "daily", "USD", "usa")


df_3n4factor_usa_usd_m = fe.french_factors("F-F_Research_Data_Factors_CSV", "monthly")
df_mom_usa_usd_m = fe.french_factors("F-F_Momentum_Factor_CSV", "monthly")

df_rf_usd_m = df_3n4factor_usa_usd_m[["rf"]]
df_3n4factor_usa_usd_m.drop(["rf"], axis=1, inplace=True)
df_3n4factor_usa_usd_m["mom"] = df_mom_usa_usd_m["mom"]

models.ThreeFourFactor.from_dataframe(df_3n4factor_usa_usd_m, "monthly", "USD", "usa")

df_3n4factor_usa_usd_a = fe.french_factors("F-F_Research_Data_Factors_CSV", "annual")
df_mom_usa_usd_a = fe.french_factors("F-F_Momentum_Factor_CSV", "annual")

df_rf_usd_a = df_3n4factor_usa_usd_a[["rf"]]
df_3n4factor_usa_usd_a.drop(["rf"], axis=1, inplace=True)
df_3n4factor_usa_usd_a["mom"] = df_mom_usa_usd_a["mom"]

models.ThreeFourFactor.from_dataframe(df_3n4factor_usa_usd_a, "annual", "USD", "usa")

# Import risk free rates USD

models.RiskFreeRate.from_dataframe(df_rf_usd_d, "daily", "USD")
models.RiskFreeRate.from_dataframe(df_rf_usd_m, "monthly", "USD")
models.RiskFreeRate.from_dataframe(df_rf_usd_a, "annual", "USD")

dict_rf_d = {"USD": df_rf_usd_d}
dict_rf_m = {"USD": df_rf_usd_m}
dict_rf_a = {"USD": df_rf_usd_a}

df_5n6factor_usa_usd_d = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_daily_CSV", "daily",
)

df_5n6factor_usa_usd_d.drop(["rf"], axis=1, inplace=True)
df_5n6factor_usa_usd_d["mom"] = df_mom_usa_usd_d["mom"]

models.FiveSixFactor.from_dataframe(df_5n6factor_usa_usd_d, "daily", "USD", "usa")

df_5n6factor_usa_usd_m = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_CSV", "monthly",
)

df_5n6factor_usa_usd_m.drop(["rf"], axis=1, inplace=True)
df_5n6factor_usa_usd_m["mom"] = df_mom_usa_usd_m["mom"]

models.FiveSixFactor.from_dataframe(df_5n6factor_usa_usd_m, "monthly", "USD", "usa")

df_5n6factor_usa_usd_a = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_CSV", "annual",
)

df_5n6factor_usa_usd_a.drop(["rf"], axis=1, inplace=True)
df_5n6factor_usa_usd_a["mom"] = df_mom_usa_usd_a["mom"]

models.FiveSixFactor.from_dataframe(df_5n6factor_usa_usd_a, "annual", "USD", "usa")

print("Currency converting factor returns for USA...")

fc_d = FactorConverter(df_fxrates_d, dict_rf_d)
fc_m = FactorConverter(df_fxrates_m, dict_rf_m)
fc_a = FactorConverter(df_fxrates_a, dict_rf_a)

for currency in currencies_fxrates:
    df_target_d = fc_d.dataframe(df_3n4factor_usa_usd_d, currency)
    df_target_m = fc_m.dataframe(df_3n4factor_usa_usd_m, currency)
    df_target_a = fc_a.dataframe(df_3n4factor_usa_usd_a, currency)

    # Create instances
    models.ThreeFourFactor.from_dataframe(df_target_d, "daily", currency, "usa")
    models.ThreeFourFactor.from_dataframe(df_target_m, "monthly", currency, "usa")
    models.ThreeFourFactor.from_dataframe(df_target_a, "annual", currency, "usa")

    df_target_d = fc_d.dataframe(df_5n6factor_usa_usd_d, currency)
    df_target_m = fc_m.dataframe(df_5n6factor_usa_usd_m, currency)
    df_target_a = fc_a.dataframe(df_5n6factor_usa_usd_a, currency)

    # Create instances
    models.FiveSixFactor.from_dataframe(df_target_d, "daily", currency, "usa")
    models.FiveSixFactor.from_dataframe(df_target_m, "monthly", currency, "usa")
    models.FiveSixFactor.from_dataframe(df_target_a, "annual", currency, "usa")

for region in regions:
    print(f"Parsing factor returns for region {region['name']}...")

    # Check if region has 5 factor data and set flag for parsing
    try:
        if region["freq"][0]["3factors"]:
            three_factor = True
        else:
            three_factor = False
    except KeyError:
        three_factor = False

    for f in region["freq"]:

        df_mom_usd = fe.french_factors(f["mom"], f["interval"])

        if three_factor:
            df_3n4factors_usd = fe.french_factors(f["3factors"], f["interval"])

            df_3n4factors_usd.drop(["rf"], axis=1, inplace=True)
            df_3n4factors_usd["mom"] = df_mom_usd["mom"]

        df_5n6factors_usd = fe.french_factors(f["5factors"], f["interval"])

        df_5n6factors_usd.drop(["rf"], axis=1, inplace=True)
        df_5n6factors_usd["mom"] = df_mom_usd["mom"]

        if f["interval"] == "daily":
            fc = fc_d
        elif f["interval"] == "monthly":
            fc = fc_m
        elif f["interval"] == "annual":
            fc = fc_a

        if three_factor:
            models.ThreeFourFactor.from_dataframe(
                df_3n4factors_usd, f["interval"], "USD", region["name"]
            )

            for currency in currencies_fxrates:
                df_converted = fc.dataframe(df_3n4factors_usd, currency)

                models.ThreeFourFactor.from_dataframe(
                    df_converted, f["interval"], currency, region["name"]
                )

        models.FiveSixFactor.from_dataframe(
            df_5n6factors_usd, f["interval"], "USD", region["name"]
        )

        for currency in currencies_fxrates:
            df_converted = fc.dataframe(df_5n6factors_usd, currency)

            models.FiveSixFactor.from_dataframe(
                df_converted, f["interval"], currency, region["name"]
            )

print("Finished data import successfully!")
