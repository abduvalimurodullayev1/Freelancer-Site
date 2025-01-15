from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/common/", include("apps.common.urls", namespace="common")),
    path("rest_framework/", include("rest_framework.urls", namespace="rest_framework")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("auth/google/", include("allauth.socialaccount.urls")),
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    path("api/v1/freelance/", include("apps.freelance.urls", namespace="freelance")),
    path("api/v1/payment/", include("apps.payment.urls", namespace="payment")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
