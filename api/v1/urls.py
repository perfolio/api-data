from django.urls import include, path
from rest_framework import routers

from . import api, views

router = routers.DefaultRouter()
router.register(r"eurrf/daily", api.DailyRiskFreeRateViewSet)
router.register(r"eurrf/monthly", api.MonthlyRiskFreeRateViewSet)
router.register(r"eurrf/annually", api.AnnuallyRiskFreeRateViewSet)
router.register(r"fxrate/daily", api.DailyExchangeRateUSDPerXViewSet)
router.register(
    r"fxrate/(?P<currency>.+)/monthly", api.MonthlyExchangeRateUSDPerXViewSet
)
router.register(r"fxrate/annually", api.AnnuallyExchangeRateUSDPerXViewSet)
router.register(r"3factor/daily", api.DailyThreeFourFactorViewSet)
router.register(r"3factor/monthly", api.MonthlyThreeFourFactorViewSet)
router.register(r"3factor/annually", api.YearlyThreeFourFactorViewSet)
router.register(r"5factor/daily", api.DailyFiveSixFactorViewSet)
router.register(r"5factor/monthly", api.MonthlyFiveSixFactorViewSet)
router.register(r"5factor/annually", api.AnnuallyFiveSixFactorViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path("", include(router.urls)),
)
