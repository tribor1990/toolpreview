from django.contrib import admin
from .models import Userjob

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('orderdate',)


admin.site.register(Userjob, JobAdmin)