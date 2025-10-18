from django.contrib import admin

from .models import Style, Image


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    pass
