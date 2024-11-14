from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/companies/', include('api.companies.urls')),
    path('api/employees/', include('api.employees.urls')),
]
