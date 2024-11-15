from core.entities.employee import Employee
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from validate_docbr import CPF as CPFValidator
from django.utils import timezone
import re


class CreateOrUpdateEmployeeUseCase:

    @staticmethod
    def validate_cpf(cpf):
        """Valida o CPF e verifica se existe algum funcionário ativo com o mesmo CPF em outra empresa."""
        cpf_validator = CPFValidator()
        if not cpf_validator.validate(cpf):
            raise ValidationError("Invalid CPF.")

        active_employee_with_cpf = Employee.objects.filter(cpf=cpf, is_active=True).exists()
        if active_employee_with_cpf:
            raise ValidationError("There is already an active employee with this CPF in another company.")

    @staticmethod
    def validate_email(cpf, email):
        """Valida o email e verifica se ele já está vinculado a outro CPF."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email.")

        email_in_use_by_other_cpf = Employee.objects.filter(~Q(cpf=cpf), email=email).exists()
        if email_in_use_by_other_cpf:
            raise ValidationError("The email is already being used by another employee.")

    @staticmethod
    def validate_phone_number(phone_number):
        """Valida o formato do número de telefone."""
        if not phone_number or not re.match(r"^\d{9}$", phone_number):
            raise ValidationError("Invalid phone number. Must contain 9 digits.")

    @staticmethod
    def validate_phone_ddd(phone_ddd):
        """Valida o formato do DDD."""
        if not phone_ddd or not re.match(r"^\d{2}$", phone_ddd):
            raise ValidationError("Invalid DDD. Must contain 2 digits.")

    @staticmethod
    def validate_phone_ddi(phone_ddi):
        """Valida o formato do DDI."""
        if not phone_ddi or not re.match(r"^\d{1,3}$", phone_ddi):
            raise ValidationError("Invalid DDI. Must contain 1 to 3 digits.")

    @staticmethod
    def validate_hire_date(hire_date):
        """Valida que a data de contratação não seja no futuro."""
        if hire_date > timezone.now().date():
            raise ValidationError("The hiring date cannot be in the future.")

    @staticmethod
    def validate_birth_date(birth_date):
        """Valida que a data de nascimento seja no passado e que o funcionário tenha pelo menos 16 anos."""
        today = timezone.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 16:
            raise ValidationError("The employee must be at least 16 years old.")
        if birth_date > today:
            raise ValidationError("The date of birth cannot be in the future.")

    @staticmethod
    def validate_existing_employee(cpf, company):
        """Verifica se o funcionário já existe na empresa e retorna erro apropriado."""
        existing_employee = Employee.objects.filter(cpf=cpf, company=company).first()
        if existing_employee:
            if existing_employee.is_active:
                raise ValidationError("This employee is already active at the company.")
            else:
                raise ValidationError("The employee registration already exists, update the employee's "
                                      "data in the company.")

    @staticmethod
    def validate_is_active_update(cpf, company, is_active, previous_is_active):
        """
        Valida a atualização do campo is_active. Se estiver sendo atualizado de False para True,
        verifica se o funcionário está ativo em outra empresa.
        """
        if not previous_is_active and is_active:
            active_in_other_company = Employee.objects.filter(cpf=cpf, is_active=True).exclude(company=company).exists()
            if active_in_other_company:
                raise ValidationError(
                    "The employee cannot be reactivated because they are already active in another company.")
