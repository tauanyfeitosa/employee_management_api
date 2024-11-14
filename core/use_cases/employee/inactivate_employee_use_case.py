from rest_framework.exceptions import ValidationError


class InactivateEmployeeUseCase:

    @staticmethod
    def validate_employee_inactivation(employee, user):
        """
        Verifica se o usuário logado tem permissão para inativar o funcionário e se o funcionário já está inativo.
        """
        if employee.company != user:
            raise ValidationError("Você não tem permissão para inativar este funcionário.")

        if not employee.is_active:
            raise ValidationError("Usuário já está inativo.")