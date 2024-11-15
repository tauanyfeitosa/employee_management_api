from django.core.exceptions import FieldError
from rest_framework import serializers
from core.entities.company import Company
from validate_docbr import CNPJ

from core.use_cases.company.get_companies_use_case import GetCompaniesUseCase


class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['cnpj', 'password', 'name', 'business_name', 'street', 'street_number',
                  'neighborhood', 'city', 'state', 'country']

    def validate_cnpj(self, value):
        """Valida o CNPJ com validate-docbr"""
        validator = CNPJ()
        if not validator.validate(value):
            raise serializers.ValidationError("Invalid CNPJ.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        company = Company.objects.create_user(password=password, **validated_data)
        return company


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['cnpj', 'name', 'business_name', 'street', 'street_number',
                  'neighborhood', 'city', 'state', 'country', 'is_active', 'is_approved']


class CompanyFilteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'cnpj', 'business_name', 'is_approved', 'is_active']

    @classmethod
    def get_filtered_queryset(cls, filters=None):
        """Chama o use case para obter o queryset filtrado."""
        use_case = GetCompaniesUseCase()
        try:
            return use_case.execute(filters=filters)
        except FieldError as e:
            raise serializers.ValidationError({"detail": str(e)})


class ApproveCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['is_approved']
        read_only_fields = ['is_approved']

    def update(self, instance, validated_data):
        if instance.is_approved:
            raise serializers.ValidationError(
                {"detail": f"The company {instance.business_name} is already approved."}
            )

        instance.is_approved = True
        instance.save()
        return instance


class InactivateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['is_active', 'is_approved']
        read_only_fields = ['is_active', 'is_approved']

    def update(self, instance, validated_data):
        if not instance.is_active:
            raise serializers.ValidationError({"detail": "The company is already inactive."})

        instance.is_active = False
        instance.save()
        return instance


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['password', 'cnpj', 'id', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            if isinstance(field, serializers.CharField):
                field.allow_blank = True

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value not in [None, '', []]:
                setattr(instance, attr, value)
        instance.save()
        return instance