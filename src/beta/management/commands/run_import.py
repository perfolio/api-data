import logging
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from beta import models
from get_data.fetch import Fetcher as fe


class Command(BaseCommand):
    help = "Imports new data from all resources"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """"""
        logging.basicConfig(level=logging.INFO, format="\u001b[32;1m%(message)s\u001b[0m")

        self.stdout.write(
            "Starting data import of factor returns, riskfree rates and exchange rates..."
        )
        """
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
        """
        return None
