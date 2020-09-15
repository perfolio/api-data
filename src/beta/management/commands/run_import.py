import logging
from typing import Any, Optional

from django.core.management.base import BaseCommand

from beta import models
from get_data.config.french import regions
from get_data.config.general import currencies_fxrates
from get_data.convert import FactorConverter
from get_data.fetch import Fetcher as fe


class Command(BaseCommand):
    help = "Imports new data from all resources"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """"""
        logging.basicConfig(level=logging.INFO, format="\u001b[32;1m%(message)s\u001b[0m")

        self.stdout.write(
            "Starting data import of factor returns, riskfree rates and exchange rates..."
        )

        # ECB Risk Free Rates #

        dict_rf = {
            "daily": {"EUR": fe.ecb_riskfreerates("daily")},
            "monthly": {"EUR": fe.ecb_riskfreerates("monthly")},
            "annual": {"EUR": fe.ecb_riskfreerates("annual")},
        }

        models.RiskFreeRate.from_dataframe(dict_rf["daily"]["EUR"], "daily", "EUR")
        models.RiskFreeRate.from_dataframe(dict_rf["monthly"]["EUR"], "monthly", "EUR")
        models.RiskFreeRate.from_dataframe(dict_rf["annual"]["EUR"], "annual", "EUR")

        # BOE Exchange Rates USD per X #

        dict_fxrates = {
            "daily": fe.boe_fxrates("daily"),
            "monthly": fe.boe_fxrates("monthly"),
            "annual": fe.boe_fxrates("annual"),
        }

        models.ExchangeRateUSDPerX.from_dataframe(dict_fxrates["daily"], "daily")
        models.ExchangeRateUSDPerX.from_dataframe(dict_fxrates["monthly"], "monthly")
        models.ExchangeRateUSDPerX.from_dataframe(dict_fxrates["annual"], "annual")

        # Kenneth French factor returns #

        fc = {}

        for region in regions:
            self.stdout.write(f"Parsing factor returns for region {region['name']}...")

            # Check if region has 3 factor data and set flag for parsing
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

                    if region["name"] == "usa":
                        dict_rf[f["interval"]]["USD"] = df_3n4factors_usd[["rf"]]

                        models.RiskFreeRate.from_dataframe(
                            dict_rf[f["interval"]]["USD"], f["interval"], "USD"
                        )

                        fc[f["interval"]] = FactorConverter(
                            dict_fxrates[f["interval"]], dict_rf[f["interval"]]
                        )

                    df_3n4factors_usd.drop(["rf"], axis=1, inplace=True)
                    df_3n4factors_usd["mom"] = df_mom_usd["mom"]

                df_5n6factors_usd = fe.french_factors(f["5factors"], f["interval"])

                df_5n6factors_usd.drop(["rf"], axis=1, inplace=True)
                df_5n6factors_usd["mom"] = df_mom_usd["mom"]

                if three_factor:
                    models.ThreeFourFactor.from_dataframe(
                        df_3n4factors_usd, f["interval"], "USD", region["name"]
                    )

                    for currency in currencies_fxrates:
                        df_converted = fc[f["interval"]].dataframe(
                            df_3n4factors_usd, currency
                        )

                        models.ThreeFourFactor.from_dataframe(
                            df_converted, f["interval"], currency, region["name"]
                        )

                models.FiveSixFactor.from_dataframe(
                    df_5n6factors_usd, f["interval"], "USD", region["name"]
                )

                for currency in currencies_fxrates:
                    df_converted = fc[f["interval"]].dataframe(
                        df_5n6factors_usd, currency
                    )

                    models.FiveSixFactor.from_dataframe(
                        df_converted, f["interval"], currency, region["name"]
                    )

        self.stdout.write("Finished data import successfully!")

        return None
