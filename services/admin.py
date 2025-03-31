# services/admin.py
from django.contrib import admin
from django.utils.html import mark_safe
from .models import ServiceCategory, Service, GalleryImage

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'display_order') # Added parent and display_order
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('parent',) # Allow filtering by parent category

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Updated list_display and added new fields/filters
    list_display = (
        'name', 'category', 'display_price_admin', 'duration', 'display_order',
        'is_extra', 'is_touch_up_refill', 'is_currently_offered', 'display_service_image'
    )
    list_filter = ('category', 'is_extra', 'is_touch_up_refill', 'is_currently_offered')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    # Updated list_editable
    list_editable = ('display_order', 'duration', 'is_extra', 'is_touch_up_refill', 'is_currently_offered')
    readonly_fields = ('display_service_image_detail', 'display_price_admin') # Show price in detail readonly

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'is_currently_offered', 'display_order')
        }),
        # Updated Details section
        ('Details & Pricing', {
            'fields': ('price', 'display_price_admin', 'duration', 'is_extra', 'is_touch_up_refill')
        }),
        ('Image', {
            'fields': ('image', 'display_service_image_detail') # Show preview in detail view
        }),
    )

    def display_service_image(self, obj):
        # Same as before
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    display_service_image.short_description = 'Image'

    def display_service_image_detail(self, obj):
        # Same as before
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image Uploaded"
    display_service_image_detail.short_description = 'Current Image Preview'

    def display_price_admin(self, obj):
        # Use the model property for display
        return obj.display_price
    display_price_admin.short_description = 'Formatted Price' # Column header in admin


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    # No changes needed here based on the prompt
    list_display = ('caption', 'category', 'uploaded_at', 'display_gallery_image')
    list_filter = ('category',)
    search_fields = ('caption', 'category__name')
    readonly_fields = ('display_gallery_image_detail',)

    fieldsets = (
        (None, {
            'fields': ('category', 'caption')
        }),
        ('Image', {
            'fields': ('image', 'display_gallery_image_detail')
        }),
    )

    def display_gallery_image(self, obj):
        # Same as before
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    display_gallery_image.short_description = 'Image Preview'

    def display_gallery_image_detail(self, obj):
        # Same as before
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image Uploaded"
    display_gallery_image_detail.short_description = 'Current Image'