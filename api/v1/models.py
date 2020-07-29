from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models


class DailyECBRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class MonthlyECBRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class AnnuallyECBRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class DailyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    EUR = DecimalField(max_digits=10, decimal_places=8)
    JPY = DecimalField(max_digits=10, decimal_places=8)
    GBP = DecimalField(max_digits=10, decimal_places=8)
    CHF = DecimalField(max_digits=10, decimal_places=8)
    RUB = DecimalField(max_digits=10, decimal_places=8)
    AUD = DecimalField(max_digits=10, decimal_places=8)
    BRL = DecimalField(max_digits=10, decimal_places=8)
    CAD = DecimalField(max_digits=10, decimal_places=8)
    CNY = DecimalField(max_digits=10, decimal_places=8)
    INR = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class MonthlyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    EUR = DecimalField(max_digits=10, decimal_places=8)
    JPY = DecimalField(max_digits=10, decimal_places=8)
    GBP = DecimalField(max_digits=10, decimal_places=8)
    CHF = DecimalField(max_digits=10, decimal_places=8)
    RUB = DecimalField(max_digits=10, decimal_places=8)
    AUD = DecimalField(max_digits=10, decimal_places=8)
    BRL = DecimalField(max_digits=10, decimal_places=8)
    CAD = DecimalField(max_digits=10, decimal_places=8)
    CNY = DecimalField(max_digits=10, decimal_places=8)
    INR = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class AnnuallyExchangeRateUSDPerX(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    EUR = DecimalField(max_digits=10, decimal_places=8)
    JPY = DecimalField(max_digits=10, decimal_places=8)
    GBP = DecimalField(max_digits=10, decimal_places=8)
    CHF = DecimalField(max_digits=10, decimal_places=8)
    RUB = DecimalField(max_digits=10, decimal_places=8)
    AUD = DecimalField(max_digits=10, decimal_places=8)
    BRL = DecimalField(max_digits=10, decimal_places=8)
    CAD = DecimalField(max_digits=10, decimal_places=8)
    CNY = DecimalField(max_digits=10, decimal_places=8)
    INR = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class DailyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class MonthlyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class YearlyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class DailyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)
    RMW = DecimalField(max_digits=10, decimal_places=8)
    CMA = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class MonthlyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)
    RMW = DecimalField(max_digits=10, decimal_places=8)
    CMA = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)



class AnnuallyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8)
    SMB = DecimalField(max_digits=10, decimal_places=8)
    HML = DecimalField(max_digits=10, decimal_places=8)
    RF = DecimalField(max_digits=10, decimal_places=8)
    RMW = DecimalField(max_digits=10, decimal_places=8)
    CMA = DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-interval',)


