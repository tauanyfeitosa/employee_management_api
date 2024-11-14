from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models.company import Company


class FilteredCompaniesViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('filtered_companies')

        # Criar e autenticar um usuário admin
        self.admin_user = get_user_model().objects.create_superuser(
            cnpj="77009125000107",
            password="adminpassword",
            name="Admin",
            business_name="Admin Company",
            street="Rua Admin",
            street_number="1",
            neighborhood="Admin Neighborhood",
            city="Admin City",
            state="Admin State",
            country="Admin Country"
        )

        # Autentica o usuário admin para todas as requisições
        self.client.force_authenticate(user=self.admin_user)

        # Criação de empresas para os testes
        self.company1 = Company.objects.create(
            cnpj="75263924000180",
            name="Empresa Teste 1",
            business_name="Teste 1 Ltda",
            street="Rua 1",
            street_number="123",
            neighborhood="Bairro 1",
            city="Cidade 1",
            state="Estado 1",
            country="País 1",
            is_active=True
        )

        self.company2 = Company.objects.create(
            cnpj="91045836000168",
            name="Empresa Teste 2",
            business_name="Teste 2 Ltda",
            street="Rua 2",
            street_number="456",
            neighborhood="Bairro 2",
            city="Cidade 2",
            state="Estado 2",
            country="País 2",
            is_active=False
        )

    def test_filter_with_nonexistent_field(self):
        """Teste para um filtro com um campo que não existe no modelo Company"""
        response = self.client.get(self.url, {'nonexistent_field': 'value'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_with_existing_field_no_results(self):
        """Teste para um filtro que existe no modelo, mas que não retorna resultados"""
        response = self.client.get(self.url, {'city': 'Cidade Inexistente'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_with_existing_field_and_results(self):
        """Teste para um filtro que existe no modelo e que encontra uma empresa"""
        response = self.client.get(self.url, {'city': 'Cidade 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['business_name'], 'Teste 1 Ltda')

    def test_filter_unauthorized(self):
        """Teste para verificar o acesso negado ao endpoint sem permissão de admin"""
        self.client.force_authenticate(user=None)  # Remove autenticação para simular acesso não autorizado
        response = self.client.get(self.url, {'city': 'Cidade 1'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
