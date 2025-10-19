from django.contrib import admin
from .models import Style, Image


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 1
    classes = ["collapse"]


class StyleAdmin(admin.ModelAdmin):
    inlines = [
        ImageAdmin,
    ]


admin.site.register(Style, StyleAdmin)
