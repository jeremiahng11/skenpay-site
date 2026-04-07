from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import RedirectView

# Customise admin branding
admin.site.site_header = "SkenPay KYC Admin"
admin.site.site_title = "SkenPay Admin"
admin.site.index_title = "KYC Applications Dashboard"

def health(request):
    return JsonResponse({"status": "ok", "service": "SkenPay KYC API"})

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/kyc/', include('kyc.urls')),
    path('health/', health),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
