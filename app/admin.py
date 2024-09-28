from django.contrib import admin

# Register your models here.
from app.models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display=["name","description","quantity","price","created_at","updated_at"]

admin.site.register(Item,ItemAdmin)