from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class ServiceCategory(models.Model):
    """Represents a category of services offered, e.g., Lashes, Microblading."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True, help_text="Unique URL-friendly identifier. Leave blank to auto-generate.")

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Service(models.Model):
    """Represents an individual service offered."""
    category = models.ForeignKey(ServiceCategory, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True, help_text="Unique URL-friendly identifier. Leave blank to auto-generate.")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True, help_text="Optional image for the service.")
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '1 hour', '90 minutes'")
    price = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '₦15,000', 'Starting from ₦20,000'") # Using CharField for flexibility (₦, ranges)
    is_active = models.BooleanField(default=True, help_text="Is this service currently offered?")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['category', 'name']
        unique_together = ('category', 'slug') # Ensure slug is unique within a category

    def __str__(self):
        return f"{self.category.name} - {self.name}"

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

    # Optional: Define a method to get the absolute URL if needed later
    # def get_absolute_url(self):
    #     return reverse('service_detail', kwargs={'category_slug': self.category.slug, 'service_slug': self.slug})


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
