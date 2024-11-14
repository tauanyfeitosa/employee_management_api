from rest_framework import serializers
from core.entities.company import Company
from validate_docbr import CNPJ


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


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'cnpj', 'business_name', 'is_active', 'is_approved']


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['password', 'cnpj', 'id', 'name']

    # Torna os campos opcionais para a atualização parcial
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            if isinstance(field, serializers.CharField):
                field.allow_blank = True

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            # Atualiza apenas se o valor não for None ou vazio
            if value not in [None, '', []]:
                setattr(instance, attr, value)
        instance.save()
        return instance