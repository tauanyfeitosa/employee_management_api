from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.entities.company import Company


class CompanyDetailViewTest(APITestCase):

    def setUp(self):

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
        self.client.force_authenticate(user=self.admin_user)

        # Criação de uma empresa para o teste
        self.company = Company.objects.create(
            cnpj="75263924000180",
            name="Empresa Teste",
            business_name="Teste Ltda",
            street="Rua Exemplo",
            street_number="123",
            neighborhood="Bairro Exemplo",
            city="Cidade Exemplo",
            state="Estado Exemplo",
            country="País Exemplo",
            is_active=True
        )

        self.detail_url_existing = reverse('company_detail', kwargs={'id': self.company.id})
        self.detail_url_nonexistent = reverse('company_detail', kwargs={'id': 9999})

    def test_retrieve_existing_company(self):
        """Teste para visualizar detalhes de uma empresa existente"""
        response = self.client.get(self.detail_url_existing)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['business_name'], self.company.business_name)

    def test_retrieve_nonexistent_company(self):
        """Teste para tentar visualizar detalhes de uma empresa inexistente"""
        response = self.client.get(self.detail_url_nonexistent)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No Company matches the given query.", response.data["detail"])
