from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['cnpj'] = self.user.cnpj
        data['is_active'] = self.user.is_active
        data['is_approved'] = self.user.is_approved

        user = self.user
        if not user.is_active:
            raise serializers.ValidationError("Sua credencial não está ativa. "
                                              "Entre em contato com o administrador do sistema!")
        if not user.is_approved:
            raise serializers.ValidationError("Sua credencial ainda não foi aprovada. "
                                              "Entre em contato com o administrador do sistema!")

        return data