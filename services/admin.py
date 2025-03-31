from django.contrib import admin
from django.utils.html import mark_safe
from .models import ServiceCategory, Service, GalleryImage

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active', 'display_service_image')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'price', 'duration')
    readonly_fields = ('display_service_image_detail',) # To show image in detail view

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'is_active')
        }),
        ('Details', {
            'fields': ('price', 'duration')
        }),
        ('Image', {
            'fields': ('image', 'display_service_image_detail') # Show preview in detail view
        }),
    )

    def display_service_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    display_service_image.short_description = 'Image Preview'

    def display_service_image_detail(self, obj):
        # For showing image preview in the detail/edit view
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image Uploaded"
    display_service_image_detail.short_description = 'Current Image'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'category', 'uploaded_at', 'display_gallery_image')
    list_filter = ('category',)
    search_fields = ('caption', 'category__name')
    readonly_fields = ('display_gallery_image_detail',) # To show image in detail view

    fieldsets = (
        (None, {
            'fields': ('category', 'caption')
        }),
        ('Image', {
            'fields': ('image', 'display_gallery_image_detail') # Show preview in detail view
        }),
    )

    def display_gallery_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    display_gallery_image.short_description = 'Image Preview'

    def display_gallery_image_detail(self, obj):
        # For showing image preview in the detail/edit view
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image Uploaded"
    display_gallery_image_detail.short_description = 'Current Image'
