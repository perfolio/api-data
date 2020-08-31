import pandas as pd
from get_data.currencies_config import currencies_fxrates
from get_data.fetch import Fetcher as fe
from get_data.convert import FactorConverter

from get_data.util import build_base_dataframes, build_model
from v1 import models
from get_data.french_config import regions
from v1.models import DailyRiskFreeRate

pd.options.mode.chained_assignment = None

# ECB Risk Free Rates #
df_rf_eur_d = fe.ecb_riskfreerates(freq="D")
df_rf_eur_d["currency"] = "EUR"
print(DailyRiskFreeRate.from_dataframe(df_rf_eur_d))
df_rf_eur_m = fe.ecb_riskfreerates(freq="M")
df_rf_eur_m["currency"] = "EUR"
build_model(model=models.MonthlyRiskFreeRate, df=df_rf_eur_m)
df_rf_eur_a = fe.ecb_riskfreerates(freq="A")
df_rf_eur_a["currency"] = "EUR"
build_model(model=models.AnnuallyRiskFreeRate, df=df_rf_eur_a)

# Possibly add riskfree rates for other currencies here
dict_rf_d = {"EUR": df_rf_eur_d}
dict_rf_m = {"EUR": df_rf_eur_m}
dict_rf_a = {"EUR": df_rf_eur_a}

# BOE Exchange Rates USD per X #

df_fxrates_d = fe.boe_fxrates(freq="D")
build_model(model=models.DailyExchangeRateUSDPerX, df=df_fxrates_d)
df_fxrates_m = fe.boe_fxrates(freq="M")
build_model(model=models.MonthlyExchangeRateUSDPerX, df=df_fxrates_m)
df_fxrates_a = fe.boe_fxrates(freq="A")
build_model(model=models.AnnuallyExchangeRateUSDPerX, df=df_fxrates_a)

# French Factor Returns #

# USA #

print("Parsing factor returns for USA...")

df_3n4factor_usa_usd_d = fe.french_factors(
    "F-F_Research_Data_Factors_daily_CSV",
    "F-F_Research_Data_Factors_daily.CSV",
    freq="D",
)
df_mom_usa_usd_d = fe.french_factors(
    "F-F_Momentum_Factor_daily_CSV", "F-F_Momentum_Factor_daily.CSV", freq="D"
)
df_3n4factor_usa_usd_d, df_rf_usd_d = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_d,
    df_mom=df_mom_usa_usd_d,
    region="USA",
    with_rf=True,
)
build_model(model=models.DailyThreeFourFactor, df=df_3n4factor_usa_usd_d)

df_3n4factor_usa_usd_m = fe.french_factors(
    "F-F_Research_Data_Factors_CSV", "F-F_Research_Data_Factors.CSV", freq="M"
)
df_mom_usa_usd_m = fe.french_factors(
    "F-F_Momentum_Factor_CSV", "F-F_Momentum_Factor.CSV", freq="M"
)
df_3n4factor_usa_usd_m, df_rf_usd_m = build_base_dataframes(
    df_factors=df_3n4factor_usa_usd_m,
    df_mom=df_mom_usa_usd_m,
    region="USA",
    with_rf=True,
)

build_model(model=models.MonthlyThreeFourFactor, df=df_3n4factor_usa_usd_m)

df_3n4factor_usa_usd_a = fe.french_factors(
    "F-F_Research_Data_Factors_CSV", "F-F_Research_Data_Factors.CSV", freq="A"
)
df_mom_usa_usd_a = fe.french_factors(
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

df_5n6factor_usa_usd_d = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_daily_CSV",
    "F-F_Research_Data_5_Factors_2x3_daily.CSV",
    freq="D",
)
df_5n6factor_usa_usd_d, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_d, df_mom=df_mom_usa_usd_d, region="USA"
)
build_model(model=models.DailyFiveSixFactor, df=df_5n6factor_usa_usd_d)

df_5n6factor_usa_usd_m = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_CSV",
    "F-F_Research_Data_5_Factors_2x3.CSV",
    freq="M",
)
df_5n6factor_usa_usd_m, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_m, df_mom=df_mom_usa_usd_m, region="USA"
)
build_model(model=models.MonthlyFiveSixFactor, df=df_5n6factor_usa_usd_m)

df_5n6factor_usa_usd_a = fe.french_factors(
    "F-F_Research_Data_5_Factors_2x3_CSV",
    "F-F_Research_Data_5_Factors_2x3.CSV",
    freq="A",
)
df_5n6factor_usa_usd_a, _ = build_base_dataframes(
    df_factors=df_5n6factor_usa_usd_a, df_mom=df_mom_usa_usd_a, region="USA"
)
build_model(model=models.AnnuallyFiveSixFactor, df=df_5n6factor_usa_usd_a)

print("Currency converting factor returns for USA...")

fc_d = FactorConverter(df_fxrates_d, df_rf_usd_d, dict_rf_d, freq="D")
fc_m = FactorConverter(df_fxrates_m, df_rf_usd_m, dict_rf_m, freq="M")
fc_a = FactorConverter(df_fxrates_a, df_rf_usd_a, dict_rf_a, freq="A")

for currency in currencies_fxrates:
    df_target_d = fc_d.dataframe(
        df_factor_source=df_3n4factor_usa_usd_d, region="USA", currency=currency,
    )
    df_target_m = fc_m.dataframe(
        df_factor_source=df_3n4factor_usa_usd_m, region="USA", currency=currency,
    )
    df_target_a = fc_a.dataframe(
        df_factor_source=df_3n4factor_usa_usd_a, region="USA", currency=currency,
    )

    # Create instances
    build_model(model=models.DailyThreeFourFactor, df=df_target_d)
    build_model(model=models.MonthlyThreeFourFactor, df=df_target_m)
    build_model(model=models.AnnuallyThreeFourFactor, df=df_target_a)

    df_target_d = fc_d.dataframe(
        df_factor_source=df_5n6factor_usa_usd_d, region="USA", currency=currency,
    )
    df_target_m = fc_m.dataframe(
        df_factor_source=df_5n6factor_usa_usd_m, region="USA", currency=currency,
    )
    df_target_a = fc_a.dataframe(
        df_factor_source=df_5n6factor_usa_usd_a, region="USA", currency=currency,
    )

    # Create instances
    build_model(model=models.DailyFiveSixFactor, df=df_target_d)
    build_model(model=models.MonthlyFiveSixFactor, df=df_target_m)
    build_model(model=models.AnnuallyFiveSixFactor, df=df_target_a)


for region in regions:
    print(f"Parsing factor returns for {region['name']}...")

    # Check if region has 5 factor data and set flag for parsing
    try:
        if region["freq"][0]["3factors"]:
            three_factor = True
        else:
            three_factor = False
    except KeyError:
        three_factor = False

    for f in region["freq"]:

        df_mom_usd = fe.french_factors(
            f["mom"], f["mom"][:-4] + ".csv", freq=f["interval"]
        )

        if three_factor:
            df_3n4factors_usd = fe.french_factors(
                f["3factors"], f["3factors"][:-4] + ".csv", freq=f["interval"]
            )

            df_3n4factors_usd, _ = build_base_dataframes(
                df_factors=df_3n4factors_usd, df_mom=df_mom_usd, region=region["name"],
            )

        df_5n6factors_usd = fe.french_factors(
            f["5factors"], f["5factors"][:-4] + ".csv", freq=f["interval"]
        )
        df_5n6factors_usd, _ = build_base_dataframes(
            df_factors=df_5n6factors_usd, df_mom=df_mom_usd, region=region["name"],
        )

        if f["interval"] == "D":
            model3n4 = models.DailyThreeFourFactor
            model5n6 = models.DailyFiveSixFactor
            fc = fc_d
        elif f["interval"] == "M":
            model3n4 = models.MonthlyThreeFourFactor
            model5n6 = models.MonthlyFiveSixFactor
            fc = fc_m
        elif f["interval"] == "A":
            model3n4 = models.AnnuallyThreeFourFactor
            model5n6 = models.AnnuallyFiveSixFactor
            fc = fc_a

        if three_factor:
            build_model(model=model3n4, df=df_3n4factors_usd)

            for currency in currencies_fxrates:
                df_converted = fc.dataframe(
                    df_factor_source=df_3n4factors_usd,
                    region=region["name"],
                    currency=currency,
                )

                build_model(model=model3n4, df=df_converted)

        build_model(model=model5n6, df=df_5n6factors_usd)

        for currency in currencies_fxrates:
            df_converted = fc.dataframe(
                df_factor_source=df_5n6factors_usd,
                region=region["name"],
                currency=currency,
            )

            build_model(model=model5n6, df=df_converted)

print("Finished data import successfully!")
