from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, Throttled
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from drf_renderer_xlsx.mixins import XLSXFileMixin
from typing import Dict, Any, Optional
from django.db.models import Model
from . import models, serializers
import re

from get_data.config.general import (
    currencies_fxrates,
    currencies_rf,
    regions,
    intervals,
    factors,
)

# Helpers #


def throttle_handler(wait):
    raise Throttled(
        detail={
            "Error": f"Request limit exceeded. Reset in {int(wait/60)} min. Create a user account and get your token or contact us for further options.",
        }
    )


def get_params(
    obj: Any, rf: bool = False, factor: Optional[int] = None
) -> Dict[str, str]:
    """
    """
    param_dict = {}
    param_dict["currency"] = obj.kwargs["currency"].upper()
    param_dict["interval"] = obj.kwargs["interval"].lower()
    param_dict["from"] = obj.request.GET.get("from")
    param_dict["to"] = obj.request.GET.get("to")
    param_dict["dropna"] = obj.request.GET.get("dropna")

    # Parsing currency
    # If rf is requested check for currencies_rf else check for currencies_fxrates
    if (rf and param_dict["currency"] not in currencies_rf) or (
        not rf and param_dict["currency"] not in currencies_fxrates
    ):
        ValidationError(
            {"Error": "Currency not supported (yet). See docs for currencies supported."}
        )
    # Parsing interval
    if param_dict["interval"] == "d":
        param_dict["interval"] = "daily"
    elif param_dict["interval"] == "m":
        param_dict["interval"] = "monthly"
    elif param_dict["interval"] == "a":
        param_dict["interval"] = "annual"
    if param_dict["interval"] not in intervals:
        ValidationError({"Error": "Invalid interval. Choose daily, monthly or annual."})

    # Parsing factors if needed
    if factor:
        param_dict["factor"] = obj.kwargs["factor"].lower()
        param_dict["region"] = obj.kwargs["region"].lower()

        if param_dict["factor"] not in factors[:factor] and param_dict["factor"] != "all":
            ValidationError({"Error": "Invalid factor. See docs for factors supported."})
        if param_dict["region"] not in regions:
            ValidationError({"Error": "Invalid region. See docs for regions supported"})

    return param_dict


def range_filter(from_: str, to_: str, interval: str, model: Model) -> Any:
    """
    """
    date_patterns = {
        "daily": "^[1,2][9,0,1][0-9][0-9]-[0,1][0-9]-[0-3][0-9]$",
        "monthly": "^[1,2][9,0,1][0-9][0-9]-[0,1][0-9](?:-[0-3][0-9])?$",
        "annual": "^[1,2][9,0,1][0-9][0-9](?:-[0,1][0-9](?:-[0-3][0-9])?)?$",
    }
    date_formats = {
        "daily": "YYYY-MM-DD",
        "monthly": "YYYY-MM or YYYY-MM-DD",
        "annual": "YYYY, YYYY-MM or YYYY-MM-DD",
    }

    if from_ is None and to_ is None:
        return model.objects.all()
    else:
        if not re.search(date_patterns[interval], from_):
            raise ValidationError(
                {
                    "Error": f"Invalid 'from' parameter. Use {date_formats[interval]} format only."
                }
            )
        if not re.search(date_patterns[interval], to_):
            raise ValidationError(
                {
                    "Error": f"Invalid 'to' parameter. Use {date_formats[interval]} format only."
                }
            )
        return model.objects.filter(period__range=[from_, to_])


class QueryTokenAuthentication(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support authentication
    via token parameter in querystring.
    """

    def authenticate(self, request):
        token = request.query_params.get("token")

        if token:
            return self.authenticate_credentials(token.strip())

        return None


class ReadOnlyAPI(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# Views #

# Risk Free Rate #


class RiskFreeRateView(XLSXFileMixin, generics.ListAPIView):
    """View for the RiskFreeRate class"""

    serializer_class = serializers.RiskFreeRateSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "rf_perfolio.xlsx"

    def get_queryset(self):
        params_dict = get_params(self, True)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.RiskFreeRate,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        return objects.exclude(rf__isnull=True)

    def throttled(self, request, wait):
        throttle_handler(wait)


# Exchange Rates #


class ExchangeRateUSDPerXView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyExchangeRateUSDPerX class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "fx_perfolio.xlsx"

    # Overwrite list method to make use of dynamic serializer
    def list(self, request, currency, interval):
        queryset = self.get_queryset()
        serializer = serializers.ExchangeRateUSDPerXSerializer(
            queryset, many=True, fields=["period", currency.upper()]
        )
        return Response(serializer.data)

    def get_queryset(self):

        params_dict = get_params(self)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ExchangeRateUSDPerX,
        )

        objects = objects.values("period", params_dict["currency"]).filter(
            interval__exact=params_dict["interval"]
        )

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        return objects.exclude(**{params_dict["currency"] + "__isnull": True})

    def throttled(self, request, wait):
        throttle_handler(wait)


# Factor returns #


class ThreeFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the ThreeFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "3factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["period", factor]}

        serializer = serializers.ThreeFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 3)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ThreeFourFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"],
            region__exact=params_dict["region"],
            interval__exact=params_dict["interval"],
        )

        if params_dict["factor"] != "all":
            objects = objects.values("period", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:3]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FourFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFourFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "4factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.FourFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 4)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.ThreeFourFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"], region__exact=params_dict["region"]
        )

        if params_dict["factor"] != "all":
            objects = objects.values("interval", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:4]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class FiveFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailyFiveFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "5factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.FiveFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 5)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.FiveSixFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"], region__exact=params_dict["region"]
        )

        if params_dict["factor"] != "all":
            objects = objects.values("interval", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:5]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)


class SixFactorView(XLSXFileMixin, generics.ListAPIView):
    """View for the DailySixFactor class"""

    permission_classes = [permissions.IsAdminUser | ReadOnlyAPI]
    authentication_classes = [QueryTokenAuthentication]
    filename = "6factor_perfolio.xlsx"

    def list(self, request, factor, region, currency, interval):
        queryset = self.get_queryset()
        fields = {}

        if factor.lower() != "all":
            fields = {"fields": ["interval", factor]}

        serializer = serializers.SixFactorSerializer(queryset, many=True, **fields)
        return Response(serializer.data)

    def get_queryset(self):
        params_dict = get_params(self, False, 6)

        objects = range_filter(
            params_dict["from"],
            params_dict["to"],
            params_dict["interval"],
            models.FiveSixFactor,
        )

        objects = objects.filter(
            currency__exact=params_dict["currency"], region__exact=params_dict["region"]
        )

        if params_dict["factor"] != "all":
            objects = objects.values("interval", params_dict["factor"])

        if params_dict["dropna"] and params_dict["dropna"].lower() == "false":
            return objects

        if params_dict["factor"] != "all":
            return objects.exclude(**{params_dict["factor"] + "__isnull": True})

        filter_fields = {}

        for f in factors[:6]:
            filter_fields[f + "__isnull"] = True

        return objects.exclude(**filter_fields)

    def throttled(self, request, wait):
        throttle_handler(wait)
