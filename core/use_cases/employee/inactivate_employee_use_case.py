from rest_framework.exceptions import ValidationError


class InactivateEmployeeUseCase:

    @staticmethod
    def validate_employee_inactivation(employee, user):
        if employee.company != user:
            raise ValidationError("User not found!")

        if not employee.is_active:
            raise ValidationError("User is already inactive.")