from rest_framework.routers import DefaultRouter
from .views import ReceiptUploadViewSet

router = DefaultRouter()
router.register("", ReceiptUploadViewSet, basename="receipts")

urlpatterns = router.urls