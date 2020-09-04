import numpy as np
import pandas as pd
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField
from django.core.exceptions import ObjectDoesNotExist
from typing import List, Dict


class RiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    period = CharField(max_length=10)
    interval = CharField(max_length=8)
    currency = CharField(max_length=3)
    rf = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-period",)
        unique_together = (
            "period",
            "interval",
            "currency",
        )

    def __eq__(self, other):
        if not isinstance(other, RiskFreeRate):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.period == other.period
            and self.interval == other.interval
            and RiskFreeRate.__compare(self.rf, other.rf)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x), np.float64(y), rtol=1e-05, atol=1e-08, equal_nan=True,
        )

    @staticmethod
    def from_dataframe(df: pd.DataFrame, interval: str, currency: str) -> None:
        """
        Create or update instances of model with data in dataframe.
        Implemented using batches of SQL queries.

        Args:
            df: The Pandas dataframe with the data to add or update.
            interval: The interval of the riskfree rates.
            currency: The currency in which the riskfree rates are.
        """

        # Change NaN to None for database NULL compatibility
        df = df.where(df.notnull(), None)

        df["interval"] = interval
        df["currency"] = currency

        update_list: List[RiskFreeRate] = []
        create_list: List[RiskFreeRate] = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            new_instance = RiskFreeRate(period=row.name, **row_dict)
            try:
                instance = RiskFreeRate.objects.get(
                    period=row.name, interval=row["interval"], currency=row["currency"]
                )
                if not instance == new_instance:
                    update_list.append(new_instance)
            except ObjectDoesNotExist:
                create_list.append(new_instance)

        # Only update database if there is something to update
        if update_list:
            RiskFreeRate.objects.bulk_update(update_list, df.columns.values.to_list())
        if create_list:
            RiskFreeRate.objects.bulk_create(create_list)

        # Print summary
        print(
            f"Created: {len(create_list)}, updated: {len(update_list)}, unchanged: {len(df.index) - len(create_list) - len(update_list)} for {interval} RiskFreeRate {currency}."
        )


class ExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    period = CharField(max_length=10)
    interval = CharField(max_length=8)
    EUR = DecimalField(max_digits=10, decimal_places=8, null=True)
    JPY = DecimalField(max_digits=10, decimal_places=8, null=True)
    GBP = DecimalField(max_digits=10, decimal_places=8, null=True)
    CHF = DecimalField(max_digits=10, decimal_places=8, null=True)
    RUB = DecimalField(max_digits=10, decimal_places=8, null=True)
    AUD = DecimalField(max_digits=10, decimal_places=8, null=True)
    BRL = DecimalField(max_digits=10, decimal_places=8, null=True)
    CAD = DecimalField(max_digits=10, decimal_places=8, null=True)
    CNY = DecimalField(max_digits=10, decimal_places=8, null=True)
    INR = DecimalField(max_digits=10, decimal_places=8, null=True)
    DKK = DecimalField(max_digits=10, decimal_places=8, null=True)
    NZD = DecimalField(max_digits=10, decimal_places=8, null=True)
    NOK = DecimalField(max_digits=10, decimal_places=8, null=True)
    SEK = DecimalField(max_digits=10, decimal_places=8, null=True)
    PLN = DecimalField(max_digits=10, decimal_places=8, null=True)
    ILS = DecimalField(max_digits=10, decimal_places=8, null=True)
    KRW = DecimalField(max_digits=10, decimal_places=8, null=True)
    TRY = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-period",)
        unique_together = (
            "period",
            "interval",
        )

    def __eq__(self, other):
        if not isinstance(other, ExchangeRateUSDPerX):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.period == other.period
            and self.interval == other.interval
            and ExchangeRateUSDPerX.__compare(self.EUR, other.EUR)
            and ExchangeRateUSDPerX.__compare(self.JPY, other.JPY)
            and ExchangeRateUSDPerX.__compare(self.GBP, other.GBP)
            and ExchangeRateUSDPerX.__compare(self.CHF, other.CHF)
            and ExchangeRateUSDPerX.__compare(self.RUB, other.RUB)
            and ExchangeRateUSDPerX.__compare(self.AUD, other.AUD)
            and ExchangeRateUSDPerX.__compare(self.BRL, other.BRL)
            and ExchangeRateUSDPerX.__compare(self.CAD, other.CAD)
            and ExchangeRateUSDPerX.__compare(self.CNY, other.CNY)
            and ExchangeRateUSDPerX.__compare(self.INR, other.INR)
            and ExchangeRateUSDPerX.__compare(self.DKK, other.DKK)
            and ExchangeRateUSDPerX.__compare(self.NZD, other.NZD)
            and ExchangeRateUSDPerX.__compare(self.NOK, other.NOK)
            and ExchangeRateUSDPerX.__compare(self.SEK, other.SEK)
            and ExchangeRateUSDPerX.__compare(self.PLN, other.PLN)
            and ExchangeRateUSDPerX.__compare(self.ILS, other.ILS)
            and ExchangeRateUSDPerX.__compare(self.KRW, other.KRW)
            and ExchangeRateUSDPerX.__compare(self.TRY, other.TRY)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x), np.float64(y), rtol=1e-05, atol=1e-08, equal_nan=True,
        )

    @staticmethod
    def from_dataframe(df: pd.DataFrame, interval: str) -> None:
        """
        Create or update instances of model with data in dataframe.
        Implemented using batches of SQL queries.

        Args:
            df: The Pandas dataframe with the data to add or update.
            interval: The interval of the fx rates.
        """

        # Change NaN to None for database NULL compatibility
        df = df.where(df.notnull(), None)

        df["interval"] = interval

        update_list: List[ExchangeRateUSDPerX] = []
        create_list: List[ExchangeRateUSDPerX] = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            new_instance = ExchangeRateUSDPerX(period=row.name, **row_dict)
            try:
                instance = ExchangeRateUSDPerX.objects.get(
                    period=row.name, interval=row["interval"]
                )
                if not instance == new_instance:
                    update_list.append(new_instance)
            except ObjectDoesNotExist:
                create_list.append(new_instance)

        # Only update database if there is something to update
        if update_list:
            ExchangeRateUSDPerX.objects.bulk_update(
                update_list, df.columns.values.to_list()
            )
        if create_list:
            ExchangeRateUSDPerX.objects.bulk_create(create_list)

        # Print summary
        print(
            f"Created: {len(create_list)}, updated: {len(update_list)}, unchanged: {len(df.index) - len(create_list) - len(update_list)} for {interval} ExchangeRateUSDPerX."
        )


class ThreeFourFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    period = CharField(max_length=10)
    interval = CharField(max_length=8)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    mktrf = DecimalField(max_digits=10, decimal_places=8, null=True)
    smb = DecimalField(max_digits=10, decimal_places=8, null=True)
    hml = DecimalField(max_digits=10, decimal_places=8, null=True)
    mom = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-period",)
        unique_together = (
            "period",
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, ThreeFourFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.period == other.period
            and self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and ThreeFourFactor.__compare(self.mktrf, other.mktrf)
            and ThreeFourFactor.__compare(self.smb, other.smb)
            and ThreeFourFactor.__compare(self.hml, other.hml)
            and ThreeFourFactor.__compare(self.mom, other.mom)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x), np.float64(y), rtol=1e-05, atol=1e-08, equal_nan=True,
        )

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame, interval: str, currency: str, region: str
    ) -> None:
        """
        Create or update instances of model with data in dataframe.
        Implemented using batches of SQL queries.

        Args:
            df: The Pandas dataframe with the data to add or update.
            interval: The interval of the factor returns.
            currency: The currency in which the factor returns are.
            region: The region for which the factor returns are.
        """

        # Change NaN to None for database NULL compatibility
        df = df.where(df.notnull(), None)

        df["interval"] = interval
        df["currency"] = currency
        df["region"] = region

        update_list: List[ThreeFourFactor] = []
        create_list: List[ThreeFourFactor] = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            new_instance = ThreeFourFactor(period=row.name, **row_dict)
            try:
                instance = ThreeFourFactor.objects.get(
                    period=row.name,
                    interval=row["interval"],
                    currency=row["currency"],
                    region=row["region"],
                )
                if not instance == new_instance:
                    update_list.append(new_instance)
            except ObjectDoesNotExist:
                create_list.append(new_instance)

        # Only update database if there is something to update
        if update_list:
            ThreeFourFactor.objects.bulk_update(update_list, df.columns.values.to_list())
        if create_list:
            ThreeFourFactor.objects.bulk_create(create_list)

        # Print summary
        print(
            f"Created: {len(create_list)}, updated: {len(update_list)}, unchanged: {len(df.index) - len(create_list) - len(update_list)} for {interval} ThreeFourFactor {region} {currency}."
        )


class FiveSixFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    period = CharField(max_length=10)
    interval = CharField(max_length=8)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    mktrf = DecimalField(max_digits=10, decimal_places=8, null=True)
    smb = DecimalField(max_digits=10, decimal_places=8, null=True)
    hml = DecimalField(max_digits=10, decimal_places=8, null=True)
    rmw = DecimalField(max_digits=10, decimal_places=8, null=True)
    cma = DecimalField(max_digits=10, decimal_places=8, null=True)
    mom = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-period",)
        unique_together = (
            "period",
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, FiveSixFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.period == other.period
            and self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and FiveSixFactor.__compare(self.mktrf, other.mktrf)
            and FiveSixFactor.__compare(self.smb, other.smb)
            and FiveSixFactor.__compare(self.hml, other.hml)
            and FiveSixFactor.__compare(self.rmw, other.rmw)
            and FiveSixFactor.__compare(self.cma, other.cma)
            and FiveSixFactor.__compare(self.mom, other.mom)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x), np.float64(y), rtol=1e-05, atol=1e-08, equal_nan=True,
        )

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame, interval: str, currency: str, region: str
    ) -> None:
        """
        Create or update instances of model with data in dataframe.
        Implemented using batches of SQL queries.

        Args:
            df: The Pandas dataframe with the data to add or update.
            interval: The interval of the factor returns.
            currency: The currency in which the factor returns are.
            region: The region for which the factor returns are.
        """

        # Change NaN to None for database NULL compatibility
        df = df.where(df.notnull(), None)

        df["interval"] = interval
        df["currency"] = currency
        df["region"] = region

        update_list: List[FiveSixFactor] = []
        create_list: List[FiveSixFactor] = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            new_instance = FiveSixFactor(period=row.name, **row_dict)
            try:
                instance = FiveSixFactor.objects.get(
                    period=row.name,
                    interval=row["interval"],
                    currency=row["currency"],
                    region=row["region"],
                )
                if not instance == new_instance:
                    update_list.append(new_instance)
            except ObjectDoesNotExist:
                create_list.append(new_instance)

        # Only update database if there is something to update
        if update_list:
            FiveSixFactor.objects.bulk_update(update_list, df.columns.values.to_list())
        if create_list:
            FiveSixFactor.objects.bulk_create(create_list)

        # Print summary
        print(
            f"Created: {len(create_list)}, updated: {len(update_list)}, unchanged: {len(df.index) - len(create_list) - len(update_list)} for {interval} FiveSixFactor {region} {currency}."
        )
