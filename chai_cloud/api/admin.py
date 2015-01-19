from django.contrib import admin
from api.models import *
# Register your models here.

class InlineInventory(admin.TabularInline):
    model = Inventory

class StoreAdmin(admin.ModelAdmin):
    inlines = [InlineInventory]

admin.site.register(Store, StoreAdmin)