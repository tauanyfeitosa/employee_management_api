from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.entities.company import Company


class CreateCompanyViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('create_company')  # Nome da URL, ajuste conforme sua configuração
        self.valid_payload = {
            "cnpj": "12345678000195",
            "name": "Empresa Teste",
            "business_name": "Empresa Teste Ltda",
            "street": "Rua Exemplo",
            "street_number": "123",
            "neighborhood": "Bairro Exemplo",
            "city": "Cidade Exemplo",
            "state": "Estado Exemplo",
            "country": "País Exemplo",
            "password": "senhaSegura123"
        }
        self.invalid_payload = {
            "cnpj": "",
            "name": "",
            "business_name": "Empresa Teste Ltda",
            "street": "Rua Exemplo",
            "street_number": "123",
            "neighborhood": "Bairro Exemplo",
            "city": "Cidade Exemplo",
            "state": "Estado Exemplo",
            "country": "País Exemplo",
            "password": "senhaSegura123"
        }
        self.invalid_cnpj_payload = {
            **self.valid_payload,
            "cnpj": "12345678000100"  # CNPJ inválido
        }

    def test_create_company_success(self):
        """Teste para criar uma empresa com dados válidos"""
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Empresa Empresa Teste Ltda cadastrada com sucesso!", response.data)

        company_exists = Company.objects.filter(cnpj=self.valid_payload["cnpj"]).exists()
        self.assertTrue(company_exists)

    def test_create_company_invalid_payload(self):
        """Teste para tentativa de criar uma empresa com dados inválidos"""
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        company_exists = Company.objects.filter(cnpj=self.invalid_payload["cnpj"]).exists()
        self.assertFalse(company_exists)

    def test_create_company_with_invalid_cnpj(self):
        """Teste para tentativa de criar uma empresa com CNPJ inválido"""
        response = self.client.post(self.url, data=self.invalid_cnpj_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid CNPJ.", str(response.data))

        company_exists = Company.objects.filter(cnpj=self.invalid_cnpj_payload["cnpj"]).exists()
        self.assertFalse(company_exists)

    def test_create_company_with_duplicate_cnpj(self):
        """Teste para tentativa de criar uma empresa com CNPJ duplicado"""
        Company.objects.create_user(
            cnpj=self.valid_payload["cnpj"],
            password=self.valid_payload["password"],
            name=self.valid_payload["name"],
            business_name=self.valid_payload["business_name"],
            street=self.valid_payload["street"],
            street_number=self.valid_payload["street_number"],
            neighborhood=self.valid_payload["neighborhood"],
            city=self.valid_payload["city"],
            state=self.valid_payload["state"],
            country=self.valid_payload["country"]
        )

        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company with this cnpj already exists.", response.data["cnpj"][0])
