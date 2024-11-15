from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.employee import Employee
from core.entities.company import Company


class UpdateEmployeeViewTest(APITestCase):

    def setUp(self):
        self.company = Company.objects.create_user(
            cnpj="77904672000156",
            password="testpassword",
            name="Test Company",
            business_name="Test Business"
        )
        self.employee = Employee.objects.create(
            cpf="91296140075",
            full_name="John Doe",
            email="johndoe@example.com",
            phone_ddd="11",
            phone_ddi="55",
            city="Aracaju",
            phone_number="912345678",
            birth_date="1995-01-01",
            hire_date="2023-01-01",
            company=self.company,
            is_active=True
        )
        self.client.force_authenticate(user=self.company)
        self.update_url = reverse('edit_employee', args=[self.employee.id])

    def test_update_employee_success(self):
        """Teste para atualização bem-sucedida de um funcionário"""
        updated_data = {
            "full_name": "John Updated Doe",
            "city": "New City"
        }
        response = self.client.patch(self.update_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.full_name, "John Updated Doe")
        self.assertEqual(self.employee.city, "New City")

    def test_update_employee_with_restricted_fields(self):
        """Teste para garantir que campos restritos não possam ser atualizados"""
        restricted_data = {
            "cpf": "00000000000",  # CPF não pode ser atualizado
        }
        response = self.client.patch(self.update_url, data=restricted_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field cannot be updated.", str(response.data["cpf"][0]))

    def test_update_employee_with_empty_fields(self):
        """Teste para garantir que uma atualização com campos vazios retorna erro"""
        empty_data = {
            "full_name": "",
            "city": ""
        }
        response = self.client.patch(self.update_url, data=empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No fields were sent for update.", str(response.data))

    def test_update_employee_invalid_email(self):
        """Teste para atualização com email inválido"""
        invalid_email_data = {
            "email": "invalid-email"  # Email inválido
        }
        response = self.client.patch(self.update_url, data=invalid_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", str(response.data["email"]))

    def test_update_employee_invalid_phone(self):
        """Teste para atualização com telefone, DDD ou DDI inválidos"""
        invalid_phone_data = {
            "phone_number": "12345678"  # Número de telefone inválido
        }
        response = self.client.patch(self.update_url, data=invalid_phone_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid phone number. Must contain 9 digits.", str(response.data["phone_number"]))

    def test_update_employee_invalid_phone_ddd(self):
        """Teste para atualização com DDD inválido"""
        invalid_phone_ddd_data = {
            "phone_ddd": "1"  # DDD inválido
        }
        response = self.client.patch(self.update_url, data=invalid_phone_ddd_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid DDD", str(response.data["phone_ddd"]))

    def test_update_employee_invalid_phone_ddi(self):
        """Teste para atualização com DDI inválido"""
        invalid_phone_ddi_data = {
            "phone_ddi": "5555"  # DDI inválido
        }
        response = self.client.patch(self.update_url, data=invalid_phone_ddi_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this field has no more than 3 characters.", str(response.data["phone_ddi"]))

    def test_update_employee_valid_partial_fields(self):
        """Teste para atualizar parcialmente com um campo válido e um campo vazio"""
        partial_data = {
            "full_name": "Jane Doe",
            "city": ""  # Campo vazio
        }
        response = self.client.patch(self.update_url, data=partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.full_name, "Jane Doe")
        self.assertNotEqual(self.employee.city, "")

    def test_update_employee_with_empty_fields(self):
        """Teste para garantir que uma atualização com todos os campos vazios retorna erro"""
        empty_data = {
            "full_name": "",
            "city": ""
        }
        response = self.client.patch(self.update_url, data=empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No fields were sent for update.", str(response.data))

    def test_update_employee_with_null_fields(self):
        """Teste para garantir que uma atualização com valores nulos retorna erro"""
        null_data = {
            "city": None
        }
        response = self.client.patch(self.update_url, data=null_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be null.", str(response.data["city"][0]))
