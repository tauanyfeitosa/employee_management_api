from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company
from django.utils import timezone
from datetime import timedelta


class CreateEmployeeViewTest(APITestCase):

    def setUp(self):
        # Configuração inicial
        self.company = Company.objects.create_user(
            cnpj="77904672000156",
            password="testpassword",
            name="Test Company",
            business_name="Test Business"
        )
        self.client.force_authenticate(user=self.company)
        self.create_url = reverse('create_employee')

    def test_create_employee_success(self):
        """Teste para criação bem-sucedida de um funcionário"""
        employee_data = {
            "cpf": "91296140075",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2023",
            "city": "São Paulo",
            "state": "SP",
            "country": "Brazil"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Employee created successfully", response.data["detail"])

    def test_create_employee_invalid_cpf(self):
        """Teste para criação de funcionário com CPF inválido"""
        employee_data = {
            "cpf": "00000000000",  # CPF inválido
            "full_name": "Jane Doe",
            "email": "janedoe@example.com",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2023"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid CPF", str(response.data))

    def test_create_employee_duplicate_active_cpf(self):
        """Teste para criação de funcionário com CPF já ativo em outra empresa"""
        Employee.objects.create(
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
        employee_data = {
            "cpf": "96650956090",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2023"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This employee is already active at the company", str(response.data))

    def test_create_employee_invalid_email(self):
        """Teste para criação de funcionário com email inválido"""
        employee_data = {
            "cpf": "76070741048",
            "full_name": "John Doe",
            "email": "invalid-email",  # Email inválido
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2023"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", str(response.data["email"]))

    def test_create_employee_duplicate_email(self):
        """Teste para criação de funcionário com email já em uso por outro CPF"""
        Employee.objects.create(
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
        employee_data = {
            "cpf": "72317671091",
            "full_name": "John Doe",
            "email": "existing@example.com",  # Email já em uso
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2023"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The email is already being used by another employee", str(response.data["email"]))

    def test_create_employee_invalid_phone_ddd(self):
        """Teste para criação de funcionário com DDD inválido"""
        employee_data = {
            "cpf": "81628627069",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "1",  # DDD inválido
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "1995-01-01",
            "hire_date": "2023-01-01"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid DDD", str(response.data["phone_ddd"]))

    def test_create_employee_invalid_phone_ddi(self):
        """Teste para criação de funcionário com DDI inválido"""
        employee_data = {
            "cpf": "81628627069",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "5555",  # DDI inválido
            "phone_number": "912345678",
            "birth_date": "1995-01-01",
            "hire_date": "2023-01-01"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this field has no more than 3 characters.", str(response.data["phone_ddi"]))

    def test_create_employee_invalid_phone_number(self):
        """Teste para criação de funcionário com número de telefone inválido"""
        employee_data = {
            "cpf": "81628627069",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "12345678",  # Número de telefone inválido
            "birth_date": "1995-01-01",
            "hire_date": "2023-01-01"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid phone number", str(response.data["phone_number"]))

    def test_create_employee_future_hire_date(self):
        """Teste para criação de funcionário com data de contratação no futuro"""
        future_date = timezone.now().date() + timedelta(days=1)
        employee_data = {
            "cpf": "23456456018",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/1995",
            "hire_date": "01/01/2025"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The hiring date cannot be in the future", str(response.data["hire_date"]))

    def test_create_employee_underage_birth_date(self):
        """Teste para criação de funcionário com data de nascimento no futuro ou idade < 16"""
        future_birth_date = timezone.now().date() + timedelta(days=1)
        employee_data = {
            "cpf": "98358496095",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "city": "Aracaju",
            "state": "SE",
            "country": "Brasil",
            "phone_ddd": "11",
            "phone_ddi": "55",
            "phone_number": "912345678",
            "birth_date": "01/01/2020",
            "hire_date": "01/01/2023"
        }
        response = self.client.post(self.create_url, data=employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The employee must be at least 16 years old", str(response.data["birth_date"]))

