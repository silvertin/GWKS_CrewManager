from django.contrib import admin

# Register your models here.
from .models import Crew

class CrewAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Crew, CrewAdmin)