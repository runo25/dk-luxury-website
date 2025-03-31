from django.contrib import admin
from .models import ContactInquiry

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_editable = ('status',) # Allow changing status directly in the list view
    readonly_fields = ('name', 'email', 'phone', 'message', 'submitted_at') # Make fields read-only in detail view

    # Control fields shown in the detail/edit view (even though they are read-only)
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'submitted_at')
        }),
        ('Inquiry Details', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status',) # Make status editable here too if needed, or keep read-only
        }),
    )

    # Prevent adding new inquiries through the admin interface
    def has_add_permission(self, request):
        return False

    # Optional: Prevent deleting inquiries through the admin interface
    # def has_delete_permission(self, request, obj=None):
    #     return False
