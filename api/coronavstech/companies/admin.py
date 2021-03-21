from django.contrib import admin

# Register your models here.

from api.coronavstech.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
