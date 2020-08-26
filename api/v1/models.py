import numpy as np
from django.db import models as models
from django.db.models import CharField, DateTimeField, DecimalField


class DailyRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10)
    currency = CharField(max_length=3)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
        )

    def __eq__(self, other):
        if not isinstance(other, DailyRiskFreeRate):
            # don't attempt to compare against other classes
            return NotImplemented

        return self.interval == other.interval and DailyRiskFreeRate.__compare(
            self.RF, other.RF
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class MonthlyRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=7)
    currency = CharField(max_length=3)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)

    def __eq__(self, other):
        if not isinstance(other, MonthlyRiskFreeRate):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and MonthlyRiskFreeRate.__compare(self.RF, other.RF)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class AnnuallyRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=4)
    currency = CharField(max_length=3)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)

    def __eq__(self, other):
        if not isinstance(other, AnnuallyRiskFreeRate):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and AnnuallyRiskFreeRate.__compare(self.RF, other.RF)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class DailyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
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
        ordering = ("-interval",)

    def __eq__(self, other):
        if not isinstance(other, DailyExchangeRateUSDPerX):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and DailyExchangeRateUSDPerX.__compare(self.EUR, other.EUR)
            and DailyExchangeRateUSDPerX.__compare(self.JPY, other.JPY)
            and DailyExchangeRateUSDPerX.__compare(self.GBP, other.GBP)
            and DailyExchangeRateUSDPerX.__compare(self.CHF, other.CHF)
            and DailyExchangeRateUSDPerX.__compare(self.RUB, other.RUB)
            and DailyExchangeRateUSDPerX.__compare(self.AUD, other.AUD)
            and DailyExchangeRateUSDPerX.__compare(self.BRL, other.BRL)
            and DailyExchangeRateUSDPerX.__compare(self.CAD, other.CAD)
            and DailyExchangeRateUSDPerX.__compare(self.CNY, other.CNY)
            and DailyExchangeRateUSDPerX.__compare(self.INR, other.INR)
            and DailyExchangeRateUSDPerX.__compare(self.DKK, other.DKK)
            and DailyExchangeRateUSDPerX.__compare(self.NZD, other.NZD)
            and DailyExchangeRateUSDPerX.__compare(self.NOK, other.NOK)
            and DailyExchangeRateUSDPerX.__compare(self.SEK, other.SEK)
            and DailyExchangeRateUSDPerX.__compare(self.PLN, other.PLN)
            and DailyExchangeRateUSDPerX.__compare(self.ILS, other.ILS)
            and DailyExchangeRateUSDPerX.__compare(self.KRW, other.KRW)
            and DailyExchangeRateUSDPerX.__compare(self.TRY, other.TRY)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class MonthlyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
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
        ordering = ("-interval",)

    def __eq__(self, other):
        if not isinstance(other, MonthlyExchangeRateUSDPerX):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and MonthlyExchangeRateUSDPerX.__compare(self.EUR, other.EUR)
            and MonthlyExchangeRateUSDPerX.__compare(self.JPY, other.JPY)
            and MonthlyExchangeRateUSDPerX.__compare(self.GBP, other.GBP)
            and MonthlyExchangeRateUSDPerX.__compare(self.CHF, other.CHF)
            and MonthlyExchangeRateUSDPerX.__compare(self.RUB, other.RUB)
            and MonthlyExchangeRateUSDPerX.__compare(self.AUD, other.AUD)
            and MonthlyExchangeRateUSDPerX.__compare(self.BRL, other.BRL)
            and MonthlyExchangeRateUSDPerX.__compare(self.CAD, other.CAD)
            and MonthlyExchangeRateUSDPerX.__compare(self.CNY, other.CNY)
            and MonthlyExchangeRateUSDPerX.__compare(self.INR, other.INR)
            and MonthlyExchangeRateUSDPerX.__compare(self.DKK, other.DKK)
            and MonthlyExchangeRateUSDPerX.__compare(self.NZD, other.NZD)
            and MonthlyExchangeRateUSDPerX.__compare(self.NOK, other.NOK)
            and MonthlyExchangeRateUSDPerX.__compare(self.SEK, other.SEK)
            and MonthlyExchangeRateUSDPerX.__compare(self.PLN, other.PLN)
            and MonthlyExchangeRateUSDPerX.__compare(self.ILS, other.ILS)
            and MonthlyExchangeRateUSDPerX.__compare(self.KRW, other.KRW)
            and MonthlyExchangeRateUSDPerX.__compare(self.TRY, other.TRY)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class AnnuallyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
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
        ordering = ("-interval",)

    def __eq__(self, other):
        if not isinstance(other, AnnuallyExchangeRateUSDPerX):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and AnnuallyExchangeRateUSDPerX.__compare(self.EUR, other.EUR)
            and AnnuallyExchangeRateUSDPerX.__compare(self.JPY, other.JPY)
            and AnnuallyExchangeRateUSDPerX.__compare(self.GBP, other.GBP)
            and AnnuallyExchangeRateUSDPerX.__compare(self.CHF, other.CHF)
            and AnnuallyExchangeRateUSDPerX.__compare(self.RUB, other.RUB)
            and AnnuallyExchangeRateUSDPerX.__compare(self.AUD, other.AUD)
            and AnnuallyExchangeRateUSDPerX.__compare(self.BRL, other.BRL)
            and AnnuallyExchangeRateUSDPerX.__compare(self.CAD, other.CAD)
            and AnnuallyExchangeRateUSDPerX.__compare(self.CNY, other.CNY)
            and AnnuallyExchangeRateUSDPerX.__compare(self.INR, other.INR)
            and AnnuallyExchangeRateUSDPerX.__compare(self.DKK, other.DKK)
            and AnnuallyExchangeRateUSDPerX.__compare(self.NZD, other.NZD)
            and AnnuallyExchangeRateUSDPerX.__compare(self.NOK, other.NOK)
            and AnnuallyExchangeRateUSDPerX.__compare(self.SEK, other.SEK)
            and AnnuallyExchangeRateUSDPerX.__compare(self.PLN, other.PLN)
            and AnnuallyExchangeRateUSDPerX.__compare(self.ILS, other.ILS)
            and AnnuallyExchangeRateUSDPerX.__compare(self.KRW, other.KRW)
            and AnnuallyExchangeRateUSDPerX.__compare(self.TRY, other.TRY)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class DailyThreeFourFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, DailyThreeFourFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and DailyThreeFourFactor.__compare(self.MktRF, other.MktRF)
            and DailyThreeFourFactor.__compare(self.SMB, other.SMB)
            and DailyThreeFourFactor.__compare(self.HML, other.HML)
            and DailyThreeFourFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class MonthlyThreeFourFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=7)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, MonthlyThreeFourFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and MonthlyThreeFourFactor.__compare(self.MktRF, other.MktRF)
            and MonthlyThreeFourFactor.__compare(self.SMB, other.SMB)
            and MonthlyThreeFourFactor.__compare(self.HML, other.HML)
            and MonthlyThreeFourFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class AnnuallyThreeFourFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=4)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, AnnuallyThreeFourFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and AnnuallyThreeFourFactor.__compare(self.MktRF, other.MktRF)
            and AnnuallyThreeFourFactor.__compare(self.SMB, other.SMB)
            and AnnuallyThreeFourFactor.__compare(self.HML, other.HML)
            and AnnuallyThreeFourFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class DailyFiveSixFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, DailyFiveSixFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and DailyFiveSixFactor.__compare(self.MktRF, other.MktRF)
            and DailyFiveSixFactor.__compare(self.SMB, other.SMB)
            and DailyFiveSixFactor.__compare(self.HML, other.HML)
            and DailyFiveSixFactor.__compare(self.RMW, other.RMW)
            and DailyFiveSixFactor.__compare(self.CMA, other.CMA)
            and DailyFiveSixFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class MonthlyFiveSixFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=7)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, MonthlyFiveSixFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and MonthlyFiveSixFactor.__compare(self.MktRF, other.MktRF)
            and MonthlyFiveSixFactor.__compare(self.SMB, other.SMB)
            and MonthlyFiveSixFactor.__compare(self.HML, other.HML)
            and MonthlyFiveSixFactor.__compare(self.RMW, other.RMW)
            and MonthlyFiveSixFactor.__compare(self.CMA, other.CMA)
            and MonthlyFiveSixFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )


class AnnuallyFiveSixFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=4)
    currency = CharField(max_length=3)
    region = CharField(max_length=21)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)
    MOM = DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        ordering = ("-interval",)
        unique_together = (
            "interval",
            "currency",
            "region",
        )

    def __eq__(self, other):
        if not isinstance(other, AnnuallyFiveSixFactor):
            # don't attempt to compare against other classes
            return NotImplemented

        return (
            self.interval == other.interval
            and self.currency == other.currency
            and self.region == other.region
            and AnnuallyFiveSixFactor.__compare(self.MktRF, other.MktRF)
            and AnnuallyFiveSixFactor.__compare(self.SMB, other.SMB)
            and AnnuallyFiveSixFactor.__compare(self.HML, other.HML)
            and AnnuallyFiveSixFactor.__compare(self.RMW, other.RMW)
            and AnnuallyFiveSixFactor.__compare(self.CMA, other.CMA)
            and AnnuallyFiveSixFactor.__compare(self.MOM, other.MOM)
        )

    @staticmethod
    def __compare(x, y):
        return np.isclose(
            np.float64(x),
            np.float64(y),
            rtol=1e-05,
            atol=1e-08,
            equal_nan=True,
        )
