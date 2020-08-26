import pandas as pd
from util import (
    build_base_dataframes,
    convert_dataframe,
    build_model,
    get_boe_exchange_rates,
    get_ecb_riskfree_rates,
    get_french_data,
)
from v1 import models
from french_config import regions

pd.options.mode.chained_assignment = None

# ECB Risk Free Rates #

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

# BOE Exchange Rates USD per X #

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

# French Factor Returns #

# USA #

print("Parsing factor returns for USA...")

df_3n4factor_usa_usd_d = get_french_data(
    "F-F_Research_Data_Factors_daily_CSV",
    "F-F_Research_Data_Factors_daily.CSV",
    freq="D",
)
df_mom_usa_usd_d = get_french_data(
    "F-F_Momentum_Factor_daily_CSV", "F-F_Momentum_Factor_daily.CSV", freq="D"
)
df_3n4factor_usa_usd_d, df_rf_usd_d = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_d,
    df_mom=df_mom_usa_usd_d,
    region="USA",
    with_rf=True,
)
build_model(model=models.DailyThreeFourFactor, df=df_3n4factor_usa_usd_d)

df_3n4factor_usa_usd_m = get_french_data(
    "F-F_Research_Data_Factors_CSV", "F-F_Research_Data_Factors.CSV", freq="M"
)
df_mom_usa_usd_m = get_french_data(
    "F-F_Momentum_Factor_CSV", "F-F_Momentum_Factor.CSV", freq="M"
)
df_3n4factor_usa_usd_m, df_rf_usd_m = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_m,
    df_mom=df_mom_usa_usd_m,
    region="USA",
    with_rf=True,
)

build_model(model=models.MonthlyThreeFourFactor, df=df_3n4factor_usa_usd_m)

df_3n4factor_usa_usd_a = get_french_data(
    "F-F_Research_Data_Factors_CSV", "F-F_Research_Data_Factors.CSV", freq="A"
)
df_mom_usa_usd_a = get_french_data(
    "F-F_Momentum_Factor_CSV", "F-F_Momentum_Factor.CSV", freq="A"
)
df_3n4factor_usa_usd_a, df_rf_usd_a = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_a,
    df_mom=df_mom_usa_usd_a,
    region="USA",
    with_rf=True,
)

build_model(model=models.AnnuallyThreeFourFactor, df=df_3n4factor_usa_usd_a)

# Build risk free rates USD
build_model(model=models.DailyRiskFreeRate, df=df_rf_usd_d)
build_model(model=models.MonthlyRiskFreeRate, df=df_rf_usd_m)
build_model(model=models.AnnuallyRiskFreeRate, df=df_rf_usd_a)

df_5n6factor_usa_usd_d = get_french_data(
    "F-F_Research_Data_5_Factors_2x3_daily_CSV",
    "F-F_Research_Data_5_Factors_2x3_daily.CSV",
    freq="D",
)
df_5n6factor_usa_usd_d, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_d, df_mom=df_mom_usa_usd_d, region="USA"
)
build_model(model=models.DailyFiveSixFactor, df=df_5n6factor_usa_usd_d)

df_5n6factor_usa_usd_m = get_french_data(
    "F-F_Research_Data_5_Factors_2x3_CSV",
    "F-F_Research_Data_5_Factors_2x3.CSV",
    freq="M",
)
df_5n6factor_usa_usd_m, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_m, df_mom=df_mom_usa_usd_m, region="USA"
)
build_model(model=models.MonthlyFiveSixFactor, df=df_5n6factor_usa_usd_m)

df_5n6factor_usa_usd_a = get_french_data(
    "F-F_Research_Data_5_Factors_2x3_CSV",
    "F-F_Research_Data_5_Factors_2x3.CSV",
    freq="A",
)
df_5n6factor_usa_usd_a, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_a, df_mom=df_mom_usa_usd_a, region="USA"
)
build_model(model=models.AnnuallyFiveSixFactor, df=df_5n6factor_usa_usd_a)

print("Currency converting factor returns for USA...")

for currency in df_fxrates_r_d.columns:
    df_target_d = convert_dataframe(
        df_factor_source=df_3n4factor_usa_usd_d,
        df_fxrates_r=df_fxrates_r_d,
        df_rf_source=df_rf_usd_d,
        dict_rf_target=dict_rf_d,
        region="USA",
        currency=currency,
    )
    df_target_m = convert_dataframe(
        df_factor_source=df_3n4factor_usa_usd_m,
        df_fxrates_r=df_fxrates_r_m,
        df_rf_source=df_rf_usd_m,
        dict_rf_target=dict_rf_m,
        region="USA",
        currency=currency,
    )
    df_target_a = convert_dataframe(
        df_factor_source=df_3n4factor_usa_usd_a,
        df_fxrates_r=df_fxrates_r_a,
        df_rf_source=df_rf_usd_a,
        dict_rf_target=dict_rf_a,
        region="USA",
        currency=currency,
    )

    # Create instances
    build_model(model=models.DailyThreeFourFactor, df=df_target_d)
    build_model(model=models.MonthlyThreeFourFactor, df=df_target_m)
    build_model(model=models.AnnuallyThreeFourFactor, df=df_target_a)

    df_target_d = convert_dataframe(
        df_factor_source=df_5n6factor_usa_usd_d,
        df_fxrates_r=df_fxrates_r_d,
        df_rf_source=df_rf_usd_d,
        dict_rf_target=dict_rf_d,
        region="USA",
        currency=currency,
    )
    df_target_m = convert_dataframe(
        df_factor_source=df_5n6factor_usa_usd_m,
        df_fxrates_r=df_fxrates_r_m,
        df_rf_source=df_rf_usd_m,
        dict_rf_target=dict_rf_m,
        region="USA",
        currency=currency,
    )
    df_target_a = convert_dataframe(
        df_factor_source=df_5n6factor_usa_usd_a,
        df_fxrates_r=df_fxrates_r_a,
        df_rf_source=df_rf_usd_a,
        dict_rf_target=dict_rf_a,
        region="USA",
        currency=currency,
    )

    # Create instances
    build_model(model=models.DailyFiveSixFactor, df=df_target_d)
    build_model(model=models.MonthlyFiveSixFactor, df=df_target_m)
    build_model(model=models.AnnuallyFiveSixFactor, df=df_target_a)


for region in regions:
    print(f"Parsing factor returns for {region['name']}...")
    for f in region["freq"]:
        df_3n4factors_usd = get_french_data(
            f["3factors"], f["3factors"][:-4] + ".csv", freq=f["interval"]
        )
        df_5n6factors_usd = get_french_data(
            f["5factors"], f["5factors"][:-4] + ".csv", freq=f["interval"]
        )
        df_mom_usd = get_french_data(
            f["mom"], f["mom"][:-4] + ".csv", freq=f["interval"]
        )

        df_3n4factors_usd, _ = build_base_dataframes(
            df_factors=df_3n4factors_usd,
            df_mom=df_mom_usd,
            region=region["name"],
        )
        df_5n6factors_usd, _ = build_base_dataframes(
            df_factors=df_5n6factors_usd,
            df_mom=df_mom_usd,
            region=region["name"],
        )

        if f["interval"] == "D":
            model3n4 = models.DailyThreeFourFactor
            model5n6 = models.DailyFiveSixFactor
            df_fxrates_r = df_fxrates_r_d
            df_rf_usd = df_rf_usd_d
            dict_rf = dict_rf_d
        elif f["interval"] == "M":
            model3n4 = models.MonthlyThreeFourFactor
            model5n6 = models.MonthlyFiveSixFactor
            df_fxrates_r = df_fxrates_r_m
            df_rf_usd = df_rf_usd_m
            dict_rf = dict_rf_m
        elif f["interval"] == "A":
            model3n4 = models.AnnuallyThreeFourFactor
            model5n6 = models.AnnuallyFiveSixFactor
            df_fxrates_r = df_fxrates_r_a
            df_rf_usd = df_rf_usd_a
            dict_rf = dict_rf_a

        build_model(model=model3n4, df=df_3n4factors_usd)
        build_model(model=model5n6, df=df_5n6factors_usd)

        for currency in df_fxrates_r.columns:
            df_converted = convert_dataframe(
                df_factor_source=df_3n4factors_usd,
                df_fxrates_r=df_fxrates_r,
                df_rf_source=df_rf_usd,
                dict_rf_target=dict_rf,
                region=region["name"],
                currency=currency,
            )

            build_model(model=model3n4, df=df_converted)

        for currency in df_fxrates_r.columns:
            df_converted = convert_dataframe(
                df_factor_source=df_5n6factors_usd,
                df_fxrates_r=df_fxrates_r,
                df_rf_source=df_rf_usd,
                dict_rf_target=dict_rf,
                region=region["name"],
                currency=currency,
            )

            build_model(model=model5n6, df=df_converted)

print("Finished data import successfully!")
