from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models.company import Company
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class AllCompaniesViewTest(APITestCase):

    def setUp(self):
        # Cria um usuário administrador e o autentica
        self.admin_user = get_user_model().objects.create_superuser(
            cnpj="12345678000195",
            password="adminpassword",
            name="Admin",
            business_name="Admin Company"
        )
        self.client.force_authenticate(user=self.admin_user)

        Company.objects.create(
            cnpj="55422914000132",
            name="Empresa 1",
            business_name="Empresa 1 Ltda",
            street="Rua 1",
            street_number="100",
            neighborhood="Bairro 1",
            city="Cidade 1",
            state="Estado 1",
            country="País 1",
            is_approved=True
        )
        Company.objects.create(
            cnpj="33996392000140",
            name="Empresa 2",
            business_name="Empresa 2 Ltda",
            street="Rua 2",
            street_number="200",
            neighborhood="Bairro 2",
            city="Cidade 2",
            state="Estado 2",
            country="País 2",
            is_approved=True
        )

        # Define a URL para o endpoint de listar todas as empresas
        self.url = reverse('all_companies')  # Nome da URL, ajuste conforme sua configuração

    def test_list_all_companies_success(self):
        """Teste para verificar o retorno de todas as empresas para um admin autenticado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica os dados retornados
        for company_data in response.data:
            self.assertIn("id", company_data)
            self.assertIn("cnpj", company_data)
            self.assertIn("business_name", company_data)

    def test_list_all_companies_no_permission(self):
        """Teste para verificar a resposta quando o usuário não é um admin"""
        non_admin_user = get_user_model().objects.create_user(
            cnpj="82409311000173",  # Exemplo de CNPJ válido
            password="senha123",
            name="Test User",
            business_name="Test Business"
        )
        self.client.force_authenticate(user=non_admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
