import pandas as pd
from typing import Dict


class FactorConverter:
    """
    A class with a collection of methods to convert factor returns in other currencies than USD.
    """

    def __init__(
        self,
        df_fxrates: pd.DataFrame,
        df_rf_usd: pd.DataFrame,
        dict_rf: Dict[str, pd.DataFrame],
        freq: str,
    ) -> None:
        """
        Create an instance of class and set all fx rate returns and riskfree rates for currency conversion.

        Args:
            df_fxrates: The Pandas dataframe with the fx rates.
            df_rf_usd: The Pandas dataframe with the riskfree rates for USD.
            dict_rf: The dictionary with Pandas dataframes with the riskfree rates for other currencies.
            freq: The frequency of the factor data. D (daily), M (monthly) or A (annually).

        Raises:
            ValueError: If invalid frequency passed.
        """

        if freq not in ["D", "M", "A"]:
            raise ValueError(
                "Invalid frequency. Choose D (daily), M (monthly) or A (annually)."
            )

        self.df_fxrates_r = round((df_fxrates / df_fxrates.shift(periods=1) - 1), 8)
        self.df_fxrates_r.drop(self.df_fxrates_r.index[:1], inplace=True)

        self.df_rf_usd = df_rf_usd
        self.dict_rf = dict_rf

    def convert_mktrf(self, s_factor_source: pd.Series, currency: str) -> pd.Series:
        """
        Convert market factor returns series following Glueck et al. (2020) to different currency.
        Defaults to USD riskfree rate if no currency-specific riskfree rate is given.

        Args:
            s_factor_source: The pandas series of factor returns in original currency
            currency: The target currency.

        Returns:
            A currency converted pandas series of factor returns
        """

        # Check if rf exists for currency given, default to USD rf
        try:
            df_rf_target = self.dict_rf[currency]
        except KeyError:
            df_rf_target = self.df_rf_usd

        return round(
            1
            / (1 + self.df_fxrates_r[currency])
            * (1 + s_factor_source + self.df_rf_usd["RF"])
            - 1
            - df_rf_target["RF"],
            4,
        )

    def convert_longShortFactor(
        self, s_factor_source: pd.Series, currency: str
    ) -> pd.Series:
        """
        Convert returns of longshort factors following Glueck et al. (2020) to different currency.

        Args:
            s_factor_source: The pandas series of factor returns in original currency
            currency: The target currency.

        Returns:
            A currency converted pandas series of factor returns
        """

        return round(1 / (1 + self.df_fxrates_r[currency]) * s_factor_source, 4)

    def convert_dataframe(
        self, df_factor_source: pd.DataFrame, region: str, currency: str
    ) -> pd.DataFrame:
        """
        Converts a Pandas dataframe with factor returns from USD to currency given.
        Wrapper method that calls specific convert methods.

        Args:
            df_factor_source: The Pandas dataframe with the original USD factor returns.
            region: The region of the factor returns.
            currency: The desired currency of the factor returns.

        Returns:
            A Pandas dataframe with the currency-converted factor returns.
        """

        df_factor_target = pd.DataFrame()
        df_factor_target["MktRF"] = self.convert_mktrf(
            df_factor_source["MktRF"], currency
        )
        df_factor_target["SMB"] = self.convert_longShortFactor(
            df_factor_source["SMB"], currency
        )
        df_factor_target["HML"] = self.convert_longShortFactor(
            df_factor_source["HML"], currency
        )
        df_factor_target["MOM"] = self.convert_longShortFactor(
            df_factor_source["MOM"], currency
        )

        if "RMW" in df_factor_source and "CMA" in df_factor_source:
            df_factor_target["RMW"] = self.convert_longShortFactor(
                df_factor_source["RMW"], currency
            )
            df_factor_target["CMA"] = self.convert_longShortFactor(
                df_factor_source["CMA"], currency
            )

        # If MktRF for given interval is NaN (most likely due to missing rf), remove instance at the beginning and the end
        df_factor_target = df_factor_target.loc[
            df_factor_target["MktRF"]
            .first_valid_index() : df_factor_target["MktRF"]
            .last_valid_index()
        ]

        # Set currency and region
        df_factor_target["currency"] = currency
        df_factor_target["region"] = region

        return df_factor_target
