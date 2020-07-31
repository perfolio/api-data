from fetch import get_french_data, get_boe_exchange_rates, get_ecb_riskfree_rates
from v1 import models
import pandas as pd

### ECB Risk Free Rates

df_ecb_d = get_ecb_riskfree_rates(freq="D")
df_ecb_m = get_ecb_riskfree_rates(freq="M")
df_ecb_a = get_ecb_riskfree_rates(freq="A")

models.DailyECBRiskFreeRate.objects.all().delete()
models.MonthlyECBRiskFreeRate.objects.all().delete()
models.AnnuallyECBRiskFreeRate.objects.all().delete()

for index, row in df_ecb_d.iterrows():
    model = models.DailyECBRiskFreeRate()
    model.interval = row.name
    model.RF = None if pd.isna(row["RF"]) else row["RF"]
    model.save()

for index, row in df_ecb_m.iterrows():
    model = models.MonthlyECBRiskFreeRate()
    model.interval = row.name
    model.RF = None if pd.isna(row["RF"]) else row["RF"]
    model.save()

for index, row in df_ecb_a.iterrows():
    model = models.AnnuallyECBRiskFreeRate()
    model.interval = row.name
    model.RF = None if pd.isna(row["RF"]) else row["RF"]
    model.save()

### BOE Exchange Rates USD per X

models.DailyExchangeRateUSDPerX.objects.all().delete()
models.MonthlyExchangeRateUSDPerX.objects.all().delete()
models.AnnuallyExchangeRateUSDPerX.objects.all().delete()

df_fxrates_d = get_boe_exchange_rates(freq="D")
df_fxrates_m = get_boe_exchange_rates(freq="M")
df_fxrates_a = get_boe_exchange_rates(freq="A")

for index, row in df_fxrates_d.iterrows():
    model = models.DailyExchangeRateUSDPerX()
    model.interval = row.name
    model.EUR = None if pd.isna(row["EUR"]) else row["EUR"]
    model.JPY = None if pd.isna(row["JPY"]) else row["JPY"]
    model.GBP = None if pd.isna(row["GBP"]) else row["GBP"]
    model.CHF = None if pd.isna(row["CHF"]) else row["CHF"]
    model.RUB = None if pd.isna(row["RUB"]) else row["RUB"]
    model.AUD = None if pd.isna(row["AUD"]) else row["AUD"]
    model.BRL = None if pd.isna(row["BRL"]) else row["BRL"] 
    model.CAD = None if pd.isna(row["CAD"]) else row["CAD"]
    model.CNY = None if pd.isna(row["CNY"]) else row["CNY"]
    model.INR = None if pd.isna(row["INR"]) else row["INR"]
    model.save()

for index, row in df_fxrates_m.iterrows():
    model = models.MonthlyExchangeRateUSDPerX()
    model.interval = row.name
    model.EUR = None if pd.isna(row["EUR"]) else row["EUR"]
    model.JPY = None if pd.isna(row["JPY"]) else row["JPY"]
    model.GBP = None if pd.isna(row["GBP"]) else row["GBP"]
    model.CHF = None if pd.isna(row["CHF"]) else row["CHF"]
    model.RUB = None if pd.isna(row["RUB"]) else row["RUB"]
    model.AUD = None if pd.isna(row["AUD"]) else row["AUD"]
    model.BRL = None if pd.isna(row["BRL"]) else row["BRL"] 
    model.CAD = None if pd.isna(row["CAD"]) else row["CAD"]
    model.CNY = None if pd.isna(row["CNY"]) else row["CNY"]
    model.INR = None if pd.isna(row["INR"]) else row["INR"]
    model.save()

for index, row in df_fxrates_a.iterrows():
    model = models.AnnuallyExchangeRateUSDPerX()
    model.interval = row.name
    model.EUR = None if pd.isna(row["EUR"]) else row["EUR"]
    model.JPY = None if pd.isna(row["JPY"]) else row["JPY"]
    model.GBP = None if pd.isna(row["GBP"]) else row["GBP"]
    model.CHF = None if pd.isna(row["CHF"]) else row["CHF"]
    model.RUB = None if pd.isna(row["RUB"]) else row["RUB"]
    model.AUD = None if pd.isna(row["AUD"]) else row["AUD"]
    model.BRL = None if pd.isna(row["BRL"]) else row["BRL"] 
    model.CAD = None if pd.isna(row["CAD"]) else row["CAD"]
    model.CNY = None if pd.isna(row["CNY"]) else row["CNY"]
    model.INR = None if pd.isna(row["INR"]) else row["INR"] 
    model.save()
