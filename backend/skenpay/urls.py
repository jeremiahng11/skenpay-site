from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os

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
    index_path = settings.BASE_DIR.parent.parent / 'frontend' / 'index.html'

    # --- DEBUG: path resolution ---
    print(f"[DEBUG] BASE_DIR          = {settings.BASE_DIR}", flush=True)
    print(f"[DEBUG] index_path        = {index_path}", flush=True)
    print(f"[DEBUG] index.html exists = {index_path.exists()}", flush=True)

    # Walk up from index_path and list each ancestor directory's contents
    for ancestor in [index_path.parent, index_path.parent.parent,
                     index_path.parent.parent.parent]:
        if ancestor.exists():
            try:
                entries = sorted(os.listdir(ancestor))
            except PermissionError:
                entries = ["<permission denied>"]
            print(f"[DEBUG] ls {ancestor} -> {entries}", flush=True)
        else:
            print(f"[DEBUG] {ancestor} does not exist", flush=True)
    # --- END DEBUG ---

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
