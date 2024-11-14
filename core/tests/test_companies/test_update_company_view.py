from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.entities.company import Company


class CompanyUpdateViewTest(APITestCase):

    def setUp(self):
        # Criação e autenticação de um usuário admin
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

        # URLs para os testes
        self.update_url_existing = reverse('company_edit', kwargs={'id': self.company.id})
        self.update_url_nonexistent = reverse('company_edit', kwargs={'id': 9999})

    def test_update_existing_company(self):
        """Teste para atualizar uma empresa existente """
        updated_data = {
            "business_name": "Teste Atualizado Ltda"
        }
        response = self.client.patch(self.update_url_existing, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se os dados foram atualizados no banco de dados
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, "Empresa Teste")
        self.assertEqual(self.company.business_name, "Teste Atualizado Ltda")

    def test_update_nonexistent_company(self):
        """Teste para tentar atualizar uma empresa inexistente"""
        updated_data = {
            "business_name": "Empresa Inexistente"
        }
        response = self.client.patch(self.update_url_nonexistent, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No Company matches the given query.", response.data["detail"])

    def test_update_with_empty_and_null_fields(self):
        """Teste para atualizar uma empresa existente com 'country' vazio"""
        original_country = self.company.country

        updated_data = {
            "country": " ",  # Espaço vazio deve ser ignorado
        }

        response = self.client.patch(self.update_url_existing, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se os campos 'country' e 'city' não foram alterados
        self.company.refresh_from_db()
        self.assertEqual(self.company.country, original_country)

    def test_update_with_null_fields(self):
        """Teste para garantir que o update com campos nulos retorne 400 Bad Request"""
        payload = {
            "business_name": "Empresa Teste Ltda Atualizada",
            "street": "Rua Nova",
            "street_number": "456",
            "neighborhood": "Bairro Atualizado",
            "city": None,  # Campo nulo
            "state": "Estado Atualizado",
            "country": "País Atualizado"
        }

        response = self.client.patch(self.update_url_existing, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be null.", response.data["city"])

        # Verifique se os campos não foram atualizados no banco de dados
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, "Empresa Teste")
        self.assertEqual(self.company.city, "Cidade Exemplo")