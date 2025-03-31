from django.shortcuts import render
from .models import ServiceCategory, Service, GalleryImage
from django.db.models import Prefetch

def services_view(request):
    """
    Displays the list of services, grouped by category.
    """
    # Fetch categories and prefetch related active services to optimize queries
    categories = ServiceCategory.objects.prefetch_related(
        Prefetch('services', queryset=Service.objects.filter(is_active=True).order_by('name'))
    ).order_by('name')

    # Filter out categories that have no active services after prefetching
    # (Alternatively, keep all categories even if empty, depending on desired display)
    categories_with_services = [cat for cat in categories if cat.services.all()]

    context = {
        'categories': categories_with_services,
    }
    return render(request, 'services/services.html', context)

def gallery_view(request):
    """
    Displays the gallery images.
    Optionally filter by category if a 'category' query parameter is present.
    """
    category_filter = request.GET.get('category') # Example: /gallery/?category=lashes
    gallery_images = GalleryImage.objects.all().order_by('-uploaded_at')
    categories = ServiceCategory.objects.all().order_by('name') # For potential filter dropdown

    if category_filter:
        gallery_images = gallery_images.filter(category__slug=category_filter)

    context = {
        'gallery_images': gallery_images,
        'categories': categories, # Pass categories for filtering UI
        'selected_category': category_filter, # Pass selected filter back to template
    }
    return render(request, 'services/gallery.html', context)
