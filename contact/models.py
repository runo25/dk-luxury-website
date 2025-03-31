from django.db import models
from django.utils import timezone

class ContactInquiry(models.Model):
    """Represents an inquiry submitted through the contact form."""

    STATUS_CHOICES = [
        ('New', 'New'),
        ('Replied', 'Replied'),
        ('Archived', 'Archived'), # Added an 'Archived' status
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Optional phone number.")
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now, editable=False) # Use default=timezone.now
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New', help_text="The status of this inquiry.")

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-submitted_at'] # Show newest inquiries first

    def __str__(self):
        return f"Inquiry from {self.name} ({self.email}) on {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
