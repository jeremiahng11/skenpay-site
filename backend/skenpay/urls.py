from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse

# Customise admin branding
admin.site.site_header = "SkenPay KYC Admin"
admin.site.site_title = "SkenPay Admin"
admin.site.index_title = "KYC Applications Dashboard"

def health(request):
    return JsonResponse({"status": "ok", "service": "SkenPay KYC API"})

def index(request):
    """Serve frontend/index.html directly via file I/O, bypassing Django's
    template loader so the path resolves correctly regardless of working
    directory or rootDirectory configuration."""
    index_path = settings.BASE_DIR.parent / 'frontend' / 'index.html'
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(
            '<h1>SkenPay KYC API</h1><p>Frontend not found.</p>',
            content_type='text/html',
            status=200,
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/kyc/', include('kyc.urls')),
    path('health/', health),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
