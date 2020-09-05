from django.urls import path, re_path
from . import api

urlpatterns = (
    # urls for Django Rest Framework API
    path("rf/<str:currency>/<str:interval>", api.RiskFreeRateView.as_view(),),
    path("fxrate/<str:currency>/<str:interval>", api.ExchangeRateUSDPerXView.as_view(),),
    path(
        "3factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.ThreeFactorView.as_view(),
    ),
    path(
        "4factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.FourFactorView.as_view(),
    ),
    path(
        "5factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.FiveFactorView.as_view(),
    ),
    path(
        "6factor/<str:factor>/<str:region>/<str:currency>/<str:interval>",
        api.SixFactorView.as_view(),
    ),
    re_path(r"^.*$", api.InvalidUrlPath.as_view()),
)
