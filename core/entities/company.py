from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from validate_docbr import CNPJ as CNPJValidator
from django.utils import timezone


class CompanyManager(BaseUserManager):
    def create_user(self, cnpj, password=None, **extra_fields):
        if not cnpj:
            raise ValueError("The CNPJ field is required")

        # Valida o CNPJ usando validate-docbr
        cnpj_validator = CNPJValidator()
        if not cnpj_validator.validate(cnpj):
            raise ValueError("Invalid CNPJ.")

        company = self.model(cnpj=cnpj, **extra_fields)
        company.set_password(password)
        company.save(using=self._db)
        return company

    def create_superuser(self, cnpj, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_approved", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(cnpj, password, **extra_fields)


class Company(AbstractBaseUser, PermissionsMixin):
    cnpj = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "cnpj"
    REQUIRED_FIELDS = ["name", "business_name"]

    objects = CompanyManager()

    def save(self, *args, **kwargs):
        if not self.is_active and self.deactivated_at is None:
            self.deactivated_at = timezone.now()
        elif self.is_active and self.deactivated_at is not None:
            self.deactivated_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Company: {self.cnpj} - {self.business_name}"
