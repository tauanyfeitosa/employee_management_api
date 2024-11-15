from django.core.exceptions import FieldError
from rest_framework import serializers
from core.entities.employee import Employee
from core.use_cases.employee.create_update_employee_use_case import CreateOrUpdateEmployeeUseCase
from core.use_cases.employee.get_employee_use_case import GetEmployeesUseCase
from core.use_cases.employee.inactivate_employee_use_case import InactivateEmployeeUseCase


class BaseEmployeeSerializer(serializers.ModelSerializer):
    """Classe base para validações comuns de Employee"""

    def validate_email(self, value):
        cpf = self.initial_data.get("cpf", None)
        CreateOrUpdateEmployeeUseCase.validate_email(cpf, value)
        return value

    def validate_phone_number(self, value):
        phone_ddd = self.initial_data.get("phone_ddd", None)
        phone_ddi = self.initial_data.get("phone_ddi", None)
        CreateOrUpdateEmployeeUseCase.validate_phone_number(value)
        return value

    def validate_phone_ddd(self, value):
        phone_number = self.initial_data.get("phone_number", None)
        phone_ddi = self.initial_data.get("phone_ddi", None)
        CreateOrUpdateEmployeeUseCase.validate_phone_ddd(value)
        return value

    def validate_phone_ddi(self, value):
        phone_number = self.initial_data.get("phone_number", None)
        phone_ddd = self.initial_data.get("phone_ddd", None)
        CreateOrUpdateEmployeeUseCase.validate_phone_ddi(value)
        return value

    def validate_hire_date(self, value):
        CreateOrUpdateEmployeeUseCase.validate_hire_date(value)
        return value

    def validate_birth_date(self, value):
        CreateOrUpdateEmployeeUseCase.validate_birth_date(value)
        return value


class CreateEmployeeSerializer(BaseEmployeeSerializer):
    class Meta:
        model = Employee
        exclude = ['company', 'created_at', 'updated_at', 'termination_date', 'is_active']

    def validate(self, data):
        cpf = data.get("cpf")
        company = self.context['request'].user
        CreateOrUpdateEmployeeUseCase.validate_existing_employee(cpf, company)
        CreateOrUpdateEmployeeUseCase.validate_cpf(cpf)
        return data


class EmployeeUpdateSerializer(BaseEmployeeSerializer):
    class Meta:
        model = Employee
        exclude = ['company', 'created_at', 'updated_at', 'cpf']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            if isinstance(field, serializers.CharField):
                field.allow_blank = True

    def validate(self, data):
        restricted_fields = {'cpf', 'company', 'created_at', 'updated_at'}

        for field in restricted_fields:
            if field in self.initial_data:
                raise serializers.ValidationError({field: "This field cannot be updated."})

        return data

    def update(self, instance, validated_data):
        if all(value in [None, '', []] for value in validated_data.values()):
            raise serializers.ValidationError("No fields were sent for update.")

        for attr, value in validated_data.items():
            if value not in [None, '', []]:
                setattr(instance, attr, value)
        instance.save()
        return instance


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['company']


class EmployeeInactivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['is_active']

    def validate(self, data):
        instance = self.instance
        user = self.context['request'].user
        InactivateEmployeeUseCase.validate_employee_inactivation(instance, user)

        return data

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.save()
        return instance


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'cpf', 'full_name', 'email', 'is_active', 'hire_date', 'termination_date']

    @staticmethod
    def get_filtered_queryset(company, filters=None):
        use_case = GetEmployeesUseCase()
        try:
            return use_case.execute(company=company, filters=filters)
        except FieldError as e:
            raise serializers.ValidationError({"detail": str(e)})

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('termination_date') is None:
            representation.pop('termination_date')
        return representation
