from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company
from django.core.exceptions import FieldError


class AllEmployeesViewTest(APITestCase):

    def setUp(self):
        self.company = Company.objects.create_user(
            cnpj="77904672000156",
            password="testpassword",
            name="Test Company",
            business_name="Test Business"
        )
        self.employee1 = Employee.objects.create(
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
        self.employee2 = Employee.objects.create(
            cpf="96824213063",
            full_name="Existing Employee",
            email="existing@example.com",
            phone_ddd="11",
            phone_ddi="55",
            phone_number="912345678",
            birth_date="1990-01-01",
            hire_date="2023-01-01",
            company=self.company
        )

        self.client.force_authenticate(user=self.company)
        self.url = reverse('list_employees')

    def test_list_all_employees_success(self):
        """Teste para listar todos os funcionários da empresa autenticada"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        for employee_data in response.data:
            self.assertIn('id', employee_data)
            self.assertIn('cpf', employee_data)
            self.assertIn('full_name', employee_data)
            self.assertIn('email', employee_data)
            self.assertIn('is_active', employee_data)
            self.assertIn('hire_date', employee_data)

    def test_access_without_authentication(self):
        """Teste para acesso à view sem autenticação"""
        self.client.force_authenticate(user=None)  # Remover autenticação
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_omit_termination_date_if_none(self):
        """Teste para garantir que 'termination_date' seja omitido quando for None"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee_data = next(emp for emp in response.data if emp['id'] == self.employee1.id)
        self.assertNotIn('termination_date', employee_data)
