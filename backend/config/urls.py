from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

api_patterns = [
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/households/", include("apps.households.urls")),
    path("api/expenses/", include("apps.expenses.urls")),
    path("api/receipts/", include("apps.receipts.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
] + api_patterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
