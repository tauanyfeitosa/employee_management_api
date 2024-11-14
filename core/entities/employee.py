from django.db import models
from core.entities.company import Company
from django.utils import timezone


class Employee(models.Model):
    cpf = models.CharField(max_length=11)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.is_active and self.termination_date is None:
            self.termination_date = timezone.now()
        elif self.is_active and self.termination_date is not None:
            self.termination_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Employee: {self.full_name} - {self.cpf}"
