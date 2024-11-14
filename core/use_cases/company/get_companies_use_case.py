from core.entities.company import Company
from django.core.exceptions import FieldError


class GetCompaniesUseCase:
    def execute(self, filters=None):
        if filters:
            # Verifica se todos os campos nos filtros existem no modelo
            valid_fields = {field.name for field in Company._meta.get_fields()}
            for key in filters.keys():
                if key not in valid_fields:
                    raise FieldError(f"Cannot resolve keyword '{key}' into field.")
            queryset = Company.objects.filter(**filters)
        else:
            queryset = Company.objects.all()
        return queryset.values('id', 'cnpj', 'business_name', 'is_approved', 'is_active')

