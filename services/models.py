# services/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
import math # For display_price formatting

class ServiceCategory(models.Model):
    """Represents a category or sub-category of services."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True, help_text="Unique URL-friendly identifier. Leave blank to auto-generate.")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL, # Keep sub-categories if parent is deleted
        related_name='children',
        help_text="Select a parent category to create a sub-category (e.g., 'Facials' under 'Spa Treatments')."
    )
    description = models.TextField(blank=True, null=True, help_text="Optional description for this category.")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which categories appear (lower numbers first).")

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['display_order', 'name'] # Order by custom order, then name

    def __str__(self):
        prefix = ""
        if self.parent:
            prefix = f"{self.parent.name} -> "
        return f"{prefix}{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure slug uniqueness globally
            original_slug = self.slug
            counter = 1
            while ServiceCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Service(models.Model):
    """Represents an individual service offered."""
    category = models.ForeignKey(
        ServiceCategory,
        related_name='services',
        on_delete=models.CASCADE,
        help_text="Select the most specific category this service belongs to (e.g., 'Classic Lashes' service under 'Main Sets' category)."
    )
    name = models.CharField(max_length=150, help_text="Specific name of the service (e.g., 'Microblading', 'Classic Refill').")
    slug = models.SlugField(max_length=160, blank=True, help_text="Unique URL-friendly identifier for this service (within its category). Leave blank to auto-generate.")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True, help_text="Optional image for the service.")
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '1 hour', '30 mins'")
    # --- PRICE CHANGE ---
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0, # Store prices like 45000, 8000 etc.
        validators=[MinValueValidator(0)],
        help_text="Enter the price in base currency units (e.g., 45000 for 45k). Do not add currency symbols or 'k'."
    )
    # --- NEW FLAGS ---
    is_extra = models.BooleanField(default=False, help_text="Check if this is an 'Extra' service (like Lash Extras).")
    is_touch_up_refill = models.BooleanField(default=False, help_text="Check if this is a Touch-up or Refill service.")
    # --- Renamed from is_active for clarity ---
    is_currently_offered = models.BooleanField(default=True, help_text="Is this service currently available to book?")
    display_order = models.PositiveIntegerField(default=0, help_text="Order within the category (lower numbers first).")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['category', 'display_order', 'name'] # Order by category, custom order, then name
        unique_together = ('category', 'slug') # Ensure slug is unique within a category

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    @property
    def display_price(self):
        """Formats the price like ₦XX,XXXk or ₦X,XXX"""
        if self.price is None:
            return "N/A"
        if self.price >= 1000:
            # Format as 'k' with comma for thousands separator within the 'k' value
            value_in_k = int(self.price / 1000)
            return f"₦{value_in_k:,}k"
        else:
            # Format lower values directly with comma separator
            return f"₦{int(self.price):,}" # Convert to int to remove potential .0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness within the category
            original_slug = self.slug
            counter = 1
            while Service.objects.filter(category=self.category, slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

# --- GalleryImage Model remains the same ---
class GalleryImage(models.Model):
    """Represents an image in the gallery, optionally linked to a service category."""
    category = models.ForeignKey(ServiceCategory, related_name='gallery_images', on_delete=models.SET_NULL, blank=True, null=True, help_text="Optional: Link image to a service category for filtering.")
    image = models.ImageField(upload_to='gallery/', help_text="The image file.")
    caption = models.CharField(max_length=255, blank=True, help_text="Optional description for the image.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.caption or f"Gallery Image {self.id}"