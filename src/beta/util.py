import re
from typing import Any, Dict, Optional

from django.db.models import Model
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import Throttled, ValidationError

from get_data.config.general import (
    currencies_fxrates,
    currencies_rf,
    factors,
    intervals,
    regions,
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
    """"""
    param_dict = {}
    param_dict["currency"] = obj.kwargs["currency"].upper()
    param_dict["interval"] = obj.kwargs["interval"].lower()
    param_dict["from"] = obj.request.GET.get("from")
    param_dict["to"] = obj.request.GET.get("to")
    param_dict["dropna"] = obj.request.GET.get("dropna")

    # Parsing currency
    # If rf is requested check for currencies_rf else check for currencies_fxrates (for factors +USD)
    if (
        (rf and param_dict["currency"] not in currencies_rf)
        or (not rf and not factor and param_dict["currency"] not in currencies_fxrates)
        or (
            not rf
            and factor
            and param_dict["currency"] not in currencies_fxrates + ["USD"]
        )
    ):
        raise ValidationError(
            {"Error": "Currency not supported (yet). See docs for currencies supported."}
        )
    if not rf and not factor and param_dict["currency"] == "USD":
        raise ValidationError({"Error": "The USD/USD fxrate is always 1."})

    # Parsing interval
    if param_dict["interval"] == "d":
        param_dict["interval"] = "daily"
    elif param_dict["interval"] == "m":
        param_dict["interval"] = "monthly"
    elif param_dict["interval"] == "a":
        param_dict["interval"] = "annual"
    if param_dict["interval"] not in intervals:
        raise ValidationError(
            {"Error": "Invalid interval. Choose daily, monthly or annual."}
        )

    # Parsing factors if needed
    if factor:
        param_dict["factor"] = obj.kwargs["factor"].lower()
        param_dict["region"] = obj.kwargs["region"].lower()

        if param_dict["factor"] not in factors[:factor] and param_dict["factor"] != "all":
            raise ValidationError(
                {"Error": "Invalid factor. See docs for factors supported."}
            )
        if param_dict["region"] not in regions:
            raise ValidationError(
                {"Error": "Invalid region. See docs for regions supported"}
            )

    return param_dict


def range_filter(from_: str, to_: str, interval: str, model: Model) -> Any:
    """"""
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
        if not from_ or not re.search(date_patterns[interval], from_):
            raise ValidationError(
                {
                    "Error": f"Invalid 'from' parameter. Use {date_formats[interval]} format only."
                }
            )
        if not to_ or not re.search(date_patterns[interval], to_):
            raise ValidationError(
                {
                    "Error": f"Invalid 'to' parameter. Use {date_formats[interval]} format only."
                }
            )

        # Parse dates in from_ and to_
        if interval == "monthly" and len(from_) == 10:
            from_ = from_[:-3]
        if interval == "monthly" and len(to_) == 10:
            to_ = to_[:-3]
        if interval == "annual" and len(from_) == 10:
            from_ = from_[:-6]
        elif interval == "annual" and len(from_) == 7:
            from_ = from_[:-3]
        if interval == "annual" and len(to_) == 10:
            to_ = to_[:-6]
        elif interval == "annual" and len(to_) == 7:
            to_ = to_[:-3]

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
