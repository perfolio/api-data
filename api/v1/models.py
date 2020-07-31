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
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class MonthlyECBRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class AnnuallyECBRiskFreeRate(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



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


    class Meta:
        ordering = ('-interval',)



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


    class Meta:
        ordering = ('-interval',)



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


    class Meta:
        ordering = ('-interval',)



class DailyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class MonthlyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class YearlyThreeFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class DailyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class MonthlyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)



class AnnuallyFiveFactor(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    interval = CharField(max_length=10, primary_key=True)
    MktRF = DecimalField(max_digits=10, decimal_places=8, null=True)
    SMB = DecimalField(max_digits=10, decimal_places=8, null=True)
    HML = DecimalField(max_digits=10, decimal_places=8, null=True)
    RF = DecimalField(max_digits=10, decimal_places=8, null=True)
    RMW = DecimalField(max_digits=10, decimal_places=8, null=True)
    CMA = DecimalField(max_digits=10, decimal_places=8, null=True)


    class Meta:
        ordering = ('-interval',)


