from django.urls import path
from .views import CreateEmployeeView, AllEmployeesView, RetrieveEmployeeView, InactivateEmployeeView, \
    FilteredEmployeesView, EmployeeUpdateView

urlpatterns = [
    path('create/', CreateEmployeeView.as_view(), name='create_employee'),
    path('all/', AllEmployeesView.as_view(), name='list_employees'),
    path('<int:pk>/', RetrieveEmployeeView.as_view(), name='retrieve_employee'),
    path('<int:pk>/inactivate/', InactivateEmployeeView.as_view(), name='inactivate_employee'),
    path('', FilteredEmployeesView.as_view(), name='filtered_employees'),
    path('<int:id>/edit/', EmployeeUpdateView.as_view(), name='edit_employee'),
]
