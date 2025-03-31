# services/views.py
from django.shortcuts import render
from .models import ServiceCategory, Service, GalleryImage
from collections import defaultdict

def services_view(request):
    """
    Displays the list of services, structured hierarchically by category and sub-category.
    """
    # Fetch all categories and currently offered services efficiently
    all_categories = list(ServiceCategory.objects.all().order_by('display_order', 'name'))
    active_services = list(Service.objects.filter(is_currently_offered=True).select_related('category').order_by('display_order', 'name'))

    # Build dictionaries for quick lookup
    categories_by_id = {cat.id: cat for cat in all_categories}
    # Initialize category data structure including empty lists for children and services
    category_data = {
        cat.id: {'category': cat, 'children': [], 'services': []}
        for cat in all_categories
    }

    # Populate services into their respective categories
    for service in active_services:
        if service.category_id in category_data:
            category_data[service.category_id]['services'].append(service)

    # Build the hierarchy: place children categories under their parents
    # We iterate backwards to potentially optimize child lookups, though not strictly necessary
    structured_data_list = []
    processed_children_ids = set()

    for category in all_categories:
        cat_id = category.id
        if category_data[cat_id]['services'] or any(child_id in category_data and (category_data[child_id]['services'] or category_data[child_id]['children']) for child_id in [c.id for c in category_data[cat_id]['category'].children.all()]): # Include if category has services OR its children have content
            if category.parent_id is None:
                # This is a top-level category
                structured_data_list.append(category_data[cat_id])
            else:
                # This is a child category, add it to its parent if parent exists
                if category.parent_id in category_data:
                    parent_data = category_data[category.parent_id]
                    # Avoid duplicates if processed via parent iteration already
                    if cat_id not in [c['category'].id for c in parent_data['children']]:
                         # Only add child if it has services itself
                        if category_data[cat_id]['services']:
                            parent_data['children'].append(category_data[cat_id])
                            processed_children_ids.add(cat_id)


    # Ensure correct ordering based on original category order for top-level
    # And sort children within parents by display_order
    final_structure = sorted(structured_data_list, key=lambda x: x['category'].display_order)
    for item in final_structure:
        item['children'].sort(key=lambda x: x['category'].display_order)


    context = {
        'service_structure': final_structure,
        # Keep gallery context if this view also handles it, otherwise remove
        # 'gallery_images': gallery_images,
        # 'categories': categories, # Pass categories for filtering UI
        # 'selected_category': category_filter, # Pass selected filter back to template
    }
    # Assuming your template is named 'services/services.html'
    return render(request, 'services/services.html', context)


# --- gallery_view remains the same ---
def gallery_view(request):
    """
    Displays the gallery images.
    Optionally filter by category if a 'category' query parameter is present.
    """
    category_filter = request.GET.get('category') # Example: /gallery/?category=lashes
    gallery_images = GalleryImage.objects.all().order_by('-uploaded_at')
    # Fetch categories that actually have gallery images associated or all if preferred
    categories_with_gallery = ServiceCategory.objects.filter(gallery_images__isnull=False).distinct().order_by('name')

    if category_filter:
        gallery_images = gallery_images.filter(category__slug=category_filter)

    context = {
        'gallery_images': gallery_images,
        'categories': categories_with_gallery, # Pass categories for filtering UI
        'selected_category': category_filter, # Pass selected filter back to template
    }
    return render(request, 'services/gallery.html', context)