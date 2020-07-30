from fetch import get_french_data, get_boe_exchange_rates, get_ecb_riskfree_rates
from v1 import models

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
    model.RF = row["RF"]
    model.save()

for index, row in df_ecb_m.iterrows():
    model = models.MonthlyECBRiskFreeRate()
    model.interval = row.name
    model.RF = row["RF"]
    model.save()

for index, row in df_ecb_a.iterrows():
    model = models.AnnuallyECBRiskFreeRate()
    model.interval = row.name
    model.RF = row["RF"]
    model.save()


### BOE Exchange Rates USD per X

df_fxrates_d = get_boe_exchange_rates(freq="D")
df_fxrates_m = get_boe_exchange_rates(freq="M")
df_fxrates_a = get_boe_exchange_rates(freq="A")

