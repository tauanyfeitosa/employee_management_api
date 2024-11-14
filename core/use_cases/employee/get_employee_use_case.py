from core.entities.employee import Employee
from django.core.exceptions import FieldError


class GetEmployeesUseCase:

    def execute(self, company, filters=None):
        if filters:
            valid_fields = {field.name for field in Employee._meta.get_fields()}
            for key in filters.keys():
                if key not in valid_fields:
                    raise FieldError(f"Cannot resolve keyword '{key}' into field.")

            queryset = Employee.objects.filter(company=company, **filters)
        else:
            queryset = Employee.objects.filter(company=company)

        return queryset.values('id', 'cpf', 'full_name', 'email', 'is_active', 'hire_date', 'termination_date')
