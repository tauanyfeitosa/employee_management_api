from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company


class InactivateEmployeeViewTest(APITestCase):

    def setUp(self):
        self.company = Company.objects.create_user(
            cnpj="77904672000156",
            password="testpassword",
            name="Test Company",
            business_name="Test Business"
        )

        self.employee = Employee.objects.create(
            cpf="96650956090",
            full_name="Active Employee",
            email="active@example.com",
            phone_ddd="11",
            phone_ddi="55",
            phone_number="912345678",
            birth_date="1995-01-01",
            hire_date="2023-01-01",
            company=self.company,
            is_active=True
        )

        self.client.force_authenticate(user=self.company)
        self.url = reverse('inactivate_employee', kwargs={'pk': self.employee.id})

    def test_inactivate_employee_success(self):
        """Teste para inativar um funcionário ativo com sucesso"""
        response = self.client.patch(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.employee.refresh_from_db()
        self.assertFalse(self.employee.is_active)

    def test_inactivate_employee_already_inactive(self):
        """Teste para tentar inativar um funcionário já inativo"""
        self.employee.is_active = False
        self.employee.save()

        response = self.client.patch(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User is already inactive.", str(response.data))

    def test_inactivate_employee_invalid_user(self):
        """Teste para tentar inativar um funcionário pertencente a outra empresa"""
        other_company = Company.objects.create_user(
            cnpj="12345678000195",
            password="otherpassword",
            name="Other Company",
            business_name="Other Business"
        )

        self.client.force_authenticate(user=other_company)

        response = self.client.patch(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User not found!", str(response.data))

    def test_access_without_authentication(self):
        """Teste para garantir que a view requer autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
