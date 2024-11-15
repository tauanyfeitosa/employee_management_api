from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company


class RetrieveEmployeeViewTest(APITestCase):

    def setUp(self):
        # Configuração inicial da empresa e funcionários
        self.company = Company.objects.create_user(
            cnpj="77904672000156",
            password="testpassword",
            name="Test Company",
            business_name="Test Business"
        )
        self.other_company = Company.objects.create_user(
            cnpj="16146158000104",
            password="otherpassword",
            name="Other Company",
            business_name="Other Business"
        )
        self.employee = Employee.objects.create(
            cpf="96650956090",
            full_name="John Doe",
            email="johndoe@example.com",
            phone_ddd="11",
            phone_ddi="55",
            phone_number="912345678",
            birth_date="1995-01-01",
            hire_date="2023-01-01",
            company=self.company,
            is_active=True
        )
        self.other_employee = Employee.objects.create(
            cpf="96824213063",
            full_name="Jane Smith",
            email="janesmith@example.com",
            phone_ddd="11",
            phone_ddi="55",
            phone_number="912345679",
            birth_date="1990-01-01",
            hire_date="2023-01-01",
            company=self.other_company
        )

        self.client.force_authenticate(user=self.company)
        self.url = reverse('retrieve_employee', args=[self.employee.id])

    def test_retrieve_employee_success(self):
        """Teste para recuperar detalhes de um funcionário com sucesso"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.employee.id)
        self.assertEqual(response.data['cpf'], self.employee.cpf)
        self.assertEqual(response.data['full_name'], self.employee.full_name)
        self.assertEqual(response.data['email'], self.employee.email)
        self.assertEqual(response.data['is_active'], self.employee.is_active)

    def test_retrieve_employee_not_found(self):
        """Teste para tentar recuperar um funcionário que não pertence à empresa"""
        url = reverse('retrieve_employee', args=[self.other_employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_access_without_authentication(self):
        """Teste para acesso à view sem autenticação"""
        self.client.force_authenticate(user=None)  # Remover autenticação
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
