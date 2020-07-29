from django.urls import reverse
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models


class ExchangeRateUSDPerX(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    interval = models.CharField(max_length=10, primary_key=True)
    EUR = models.DecimalField(max_digits=10, decimal_places=8)
    JPY = models.DecimalField(max_digits=10, decimal_places=8)
    GBP = models.DecimalField(max_digits=10, decimal_places=8)
    CHF = models.DecimalField(max_digits=10, decimal_places=8)
    RUB = models.DecimalField(max_digits=10, decimal_places=8)
    AUD = models.DecimalField(max_digits=10, decimal_places=8)
    BRL = models.DecimalField(max_digits=10, decimal_places=8)
    CAD = models.DecimalField(max_digits=10, decimal_places=8)
    CNY = models.DecimalField(max_digits=10, decimal_places=8)
    INR = models.DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('v1_exchangerateusdperx_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('v1_exchangerateusdperx_update', args=(self.pk,))


class ECBRiskFreeRate(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    interval = models.CharField(max_length=10, primary_key=True)
    RF = models.DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('v1_ecbriskfreerate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('v1_ecbriskfreerate_update', args=(self.pk,))


class ThreeFactor(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    interval = models.CharField(max_length=10, primary_key=True)
    MktRF = models.DecimalField(max_digits=10, decimal_places=8)
    SMB = models.DecimalField(max_digits=10, decimal_places=8)
    HML = models.DecimalField(max_digits=10, decimal_places=8)
    RF = models.DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('v1_threefactor_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('v1_threefactor_update', args=(self.pk,))


class FiveFactor(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    RMW = models.DecimalField(max_digits=10, decimal_places=8)
    CMA = models.DecimalField(max_digits=10, decimal_places=8)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('v1_fivefactor_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('v1_fivefactor_update', args=(self.pk,))

