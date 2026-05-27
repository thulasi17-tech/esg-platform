from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path(
        'api/auth/login/',
        TokenObtainPairView.as_view()
    ),

    path(
        'api/auth/refresh/',
        TokenRefreshView.as_view()
    ),

    path('api/companies/', include('companies.urls')),

    path('api/ingestion/', include('ingestion.urls')),

    path('api/emissions/', include('emissions.urls')),

    path('api/audits/', include('audits.urls')),

    path('api/users/', include('users.urls')),
]