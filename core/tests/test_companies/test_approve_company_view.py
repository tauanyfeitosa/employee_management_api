from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.company import Company
from django.contrib.auth import get_user_model


class ApproveCompanyViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            cnpj="12345678000195",
            password="adminpassword",
            name="Admin",
            business_name="Admin Company"
        )
        self.client.force_authenticate(user=self.user)

        self.company = Company.objects.create(
            cnpj="98765432000195",
            name="Empresa Teste",
            business_name="Empresa Teste Ltda",
            street="Rua Exemplo",
            street_number="123",
            neighborhood="Bairro Exemplo",
            city="Cidade Exemplo",
            state="Estado Exemplo",
            country="País Exemplo",
            is_approved=False
        )
        self.url = reverse('approve_company', kwargs={'pk': self.company.pk})

    def test_approve_company_success(self):
        """Teste de aprovação bem-sucedida de uma empresa"""
        response = self.client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(f"A empresa {self.company.business_name} foi aprovada com sucesso!", response.data["message"])

        self.company.refresh_from_db()
        self.assertTrue(self.company.is_approved)

    def test_approve_company_already_approved(self):
        """Teste para empresa que já está aprovada"""
        self.company.is_approved = True
        self.company.save()

        response = self.client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(f"A empresa {self.company.business_name} já está aprovada.", response.data["message"])

    def test_approve_company_not_found(self):
        """Teste para empresa que não existe"""
        url = reverse('approve_company', kwargs={'pk': 9999})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No Company matches the given query.", response.data["detail"])
