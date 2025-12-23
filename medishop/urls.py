from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # # smart role-based redirect (logo / login redirect)
    # path("", include("main.urls")),

    # apps
    path("users/", include("users.urls")),
    path("manager/", include("managers.urls")),
    path("", include("customers.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
