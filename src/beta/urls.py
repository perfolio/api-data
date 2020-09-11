from django.urls import path, re_path

from . import api

urlpatterns = (
    # urls for Django Rest Framework API
    path("rf/<str:currency>/<str:interval>", api.RiskFreeRateView.as_view(), name="rf"),
    path(
        "fxrate/<str:currency>/<str:interval>",
        api.ExchangeRateUSDPerXView.as_view(),
        name="fxrate",
    ),
    path(
        "3factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.ThreeFactorView.as_view(),
        name="3factor",
    ),
    path(
        "4factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.FourFactorView.as_view(),
        name="4factor",
    ),
    path(
        "5factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.FiveFactorView.as_view(),
        name="5factor",
    ),
    path(
        "6factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.SixFactorView.as_view(),
        name="6factor",
    ),
    re_path(r"^.*$", api.InvalidUrlPath.as_view(), name="catch-all"),
)
