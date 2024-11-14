from django.db import models
from core.models.company import Company

class Employee(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_ddi = models.CharField(max_length=3)
    phone_ddd = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=9)
    birth_date = models.DateField()
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Employee: {self.full_name} - {self.cpf}"
