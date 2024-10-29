from django.contrib import admin
from .models import Category, Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category')

admin.site.register(Event, EventAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)