from django.contrib import admin
from api.models import *
# Register your models here.

class InlineInventory(admin.TabularInline):
    model = Inventory
    verbose_name = "Inventory Item"
    verbose_name_plural = "Inventory"

class StoreAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Store Name:', {'fields': ['name']}),
        ('Active', {'fields': ['active']}),
    ]
    inlines = [InlineInventory]

class InlineOptions(admin.TabularInline):
    model = Option

class MenuAdmin(admin.ModelAdmin):
    inlines = [InlineOptions]

admin.site.register(Store, StoreAdmin)
admin.site.register(Menu, MenuAdmin)