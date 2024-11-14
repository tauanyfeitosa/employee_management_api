from django.contrib import admin
from core.entities.employee import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpf', 'full_name', 'email', 'company', 'is_active', 'hire_date', 'termination_date')
    list_filter = ('is_active', 'company', 'state', 'country')
    search_fields = ('cpf', 'full_name', 'email', 'company__business_name')
    ordering = ('-hire_date',)
    readonly_fields = ('created_at', 'updated_at', 'termination_date')
    date_hierarchy = 'hire_date'


    fieldsets = (
        (None, {
            'fields': ('cpf', 'full_name', 'email', 'birth_date', 'hire_date', 'termination_date')
        }),
        ('Contato', {
            'fields': ('phone_ddi', 'phone_ddd', 'phone_number', 'city', 'state', 'country')
        }),
        ('Empresa e Status', {
            'fields': ('company', 'is_active')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)


admin.site.register(Employee, EmployeeAdmin)

