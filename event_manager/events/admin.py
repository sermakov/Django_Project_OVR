from django.contrib import admin
from .models import Category, Event
from django.utils.html import format_html

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'display_image')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    ordering = ('date',)
    readonly_fields = ('display_image_preview',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date', 'location', 'category')
        }),
        ('Media', {
            'fields': ('main_image', 'display_image_preview', 'document')
        }),
    )

    def display_image(self, obj):
        if obj.main_image:
            return 'Да'
        return 'Нет'
    display_image.short_description = 'Изображение'

    def display_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.main_image.url)
        return 'Нет изображения'
    display_image_preview.short_description = 'Предпросмотр изображения'

admin.site.register(Event, EventAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)