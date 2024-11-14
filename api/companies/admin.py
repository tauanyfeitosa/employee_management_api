from django.contrib import admin
from core.models.company import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'cnpj', 'business_name', 'name', 'is_active_status', 'approval_status')
    search_fields = ('cnpj', 'business_name', 'name')
    list_filter = ('is_approved', 'is_active')

    def is_active_status(self, obj):
        return "Ativa" if obj.is_active else "Inativa"
    is_active_status.short_description = 'Ativa'

    def approval_status(self, obj):
        return "Aprovada" if obj.is_approved else "Em espera"
    approval_status.short_description = 'Status de Aprovação'

