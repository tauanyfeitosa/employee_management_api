from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company


class FilteredEmployeesViewTest(APITestCase):

    def setUp(self):
        # Configuração inicial da empresa e funcionários
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
            full_name="Inactive Employee",
            email="inactive@example.com",
            phone_ddd="11",
            phone_ddi="55",
            phone_number="912345678",
            birth_date="1990-01-01",
            hire_date="2023-01-01",
            termination_date="2023-06-01",
            company=self.company,
            is_active=False
        )

        self.client.force_authenticate(user=self.company)
        self.url = reverse('filtered_employees')

    def test_list_employees_with_valid_filter(self):
        """Teste para listar funcionários com filtro válido"""
        response = self.client.get(self.url, {'is_active': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cpf'], self.employee1.cpf)
        self.assertIn('id', response.data[0])
        self.assertIn('full_name', response.data[0])
        self.assertIn('email', response.data[0])
        self.assertIn('is_active', response.data[0])
        self.assertIn('hire_date', response.data[0])

    def test_list_employees_with_invalid_filter(self):
        """Teste para erro ao usar um campo de filtro inválido"""
        response = self.client.get(self.url, {'invalid_field': 'value'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot resolve keyword", str(response.data["detail"]))

    def test_access_without_authentication(self):
        """Teste para acesso à view sem autenticação"""
        self.client.force_authenticate(user=None)  # Remover autenticação
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_omit_termination_date_if_none(self):
        """Teste para garantir que 'termination_date' seja omitido quando for None"""
        response = self.client.get(self.url, {'is_active': 'True'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee_data = response.data[0]
        self.assertNotIn('termination_date', employee_data)

    def test_include_termination_date_if_present(self):
        """Teste para garantir que 'termination_date' seja incluído se não for None"""
        response = self.client.get(self.url, {'is_active': 'False'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('termination_date', response.data[0])
        self.assertEqual(response.data[0]['termination_date'], "01/06/2023")
