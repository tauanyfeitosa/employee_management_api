from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.entities.company import Company


class InactivateCompanyViewTest(APITestCase):

    def setUp(self):
        # Cria um usuário admin e autentica
        self.admin_user = get_user_model().objects.create_superuser(
            cnpj="11222333000181",
            password="adminpassword",
            name="Admin",
            business_name="Admin Company"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Cria uma empresa ativa para os testes
        self.company = Company.objects.create(
            cnpj="12345678000195",
            name="Empresa Ativa",
            business_name="Empresa Ativa Ltda",
            street="Rua Ativa",
            street_number="123",
            neighborhood="Bairro Ativo",
            city="Cidade Ativa",
            state="Estado Ativo",
            country="País Ativo",
            is_active=True,
            is_approved=True
        )

        # Cria uma empresa inativa para os testes de erro
        self.inactive_company = Company.objects.create(
            cnpj="98765432000195",
            name="Empresa Inativa",
            business_name="Empresa Inativa Ltda",
            street="Rua Inativa",
            street_number="456",
            neighborhood="Bairro Inativo",
            city="Cidade Inativa",
            state="Estado Inativo",
            country="País Inativo",
            is_active=False,
            is_approved=False
        )

    def test_inactivate_nonexistent_company(self):
        """Teste para tentar inativar uma empresa que não existe"""
        url = reverse('inactivate_company', kwargs={'pk': 9999})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactivate_active_company(self):
        """Teste para inativar uma empresa ativa com sucesso"""
        url = reverse('inactivate_company', kwargs={'pk': self.company.pk})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["detail"], "Company successfully inactivated!")

        self.company.refresh_from_db()
        self.assertFalse(self.company.is_active)
        self.assertFalse(self.company.is_approved)

    def test_inactivate_already_inactive_company(self):
        """Teste para tentar inativar uma empresa que já está inativa"""
        url = reverse('inactivate_company', kwargs={'pk': self.inactive_company.pk})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "The company is already inactive.")
