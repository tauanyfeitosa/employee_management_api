from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (CreateCompanyView, ApproveCompanyView, CustomTokenObtainPairView,
                    FilteredCompaniesView, AllCompaniesView, CompanyDetailView, CompanyUpdateView,
                    InactivateCompanyView)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create/", CreateCompanyView.as_view(), name="create_company"),
    path('<int:pk>/approve/', ApproveCompanyView.as_view(), name='approve_company'),
    path('', FilteredCompaniesView.as_view(), name='filtered_companies'),
    path('all/', AllCompaniesView.as_view(), name='all_companies'),
    path('<int:id>/', CompanyDetailView.as_view(), name='company_detail'),
    path('<int:id>/edit/', CompanyUpdateView.as_view(), name='company_edit'),
    path('<int:pk>/inactivate/', InactivateCompanyView.as_view(), name='inactivate_company'),
]