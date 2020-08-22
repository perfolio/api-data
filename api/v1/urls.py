from django.urls import include, path
from rest_framework import routers

from . import api, views

router = routers.DefaultRouter()
router.register(r"rf/(?P<currency>.+)/daily", api.DailyRiskFreeRateViewSet)
router.register(r"rf/(?P<currency>.+)/monthly", api.MonthlyRiskFreeRateViewSet)
router.register(
    r"rf/(?P<currency>.+)/annually", api.AnnuallyRiskFreeRateViewSet
)
router.register(
    r"fxrate/(?P<currency>.+)/daily", api.DailyExchangeRateUSDPerXViewSet
)
router.register(
    r"fxrate/(?P<currency>.+)/monthly", api.MonthlyExchangeRateUSDPerXViewSet
)
router.register(
    r"fxrate/(?P<currency>.+)/annually", api.AnnuallyExchangeRateUSDPerXViewSet
)
router.register(r"3factor/(?P<currency>.+)/daily", api.DailyThreeFactorViewSet)
router.register(
    r"3factor/(?P<currency>.+)/monthly", api.MonthlyThreeFactorViewSet
)
router.register(
    r"3factor/(?P<currency>.+)/annually", api.AnnuallyThreeFactorViewSet
)
router.register(r"4factor/(?P<currency>.+)/daily", api.DailyFourFactorViewSet)
router.register(
    r"4factor/(?P<currency>.+)/monthly", api.MonthlyFourFactorViewSet
)
router.register(
    r"4factor/(?P<currency>.+)/annually", api.AnnuallyFourFactorViewSet
)
router.register(r"5factor/(?P<currency>.+)/daily", api.DailyFiveFactorViewSet)
router.register(
    r"5factor/(?P<currency>.+)/monthly", api.MonthlyFiveFactorViewSet
)
router.register(
    r"5factor/(?P<currency>.+)/annually", api.AnnuallyFiveFactorViewSet
)
router.register(r"6factor/(?P<currency>.+)/daily", api.DailySixFactorViewSet)
router.register(
    r"6factor/(?P<currency>.+)/monthly", api.MonthlySixFactorViewSet
)
router.register(
    r"6factor/(?P<currency>.+)/annually", api.AnnuallySixFactorViewSet
)
router.register(
    r"factor/(?P<factor>.+)/(?P<currency>.+)/daily", api.DailyFactorViewSet
)
router.register(
    r"factor/(?P<factor>.+)/(?P<currency>.+)/monthly", api.MonthlyFactorViewSet
)
router.register(
    r"factor/(?P<factor>.+)/(?P<currency>.+)/annually",
    api.AnnuallyFactorViewSet,
)

urlpatterns = (
    # urls for Django Rest Framework API
    path("", include(router.urls)),
)
