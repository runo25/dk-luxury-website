from django.urls import path
from . import views

app_name = 'services' # Namespace for URLs

urlpatterns = [
    path('', views.services_view, name='service_list'), # URL for the main services page
    path('gallery/', views.gallery_view, name='gallery'), # URL for the gallery page
    # Example for a potential future detail view (requires model changes and view logic)
    # path('<slug:category_slug>/<slug:service_slug>/', views.service_detail_view, name='service_detail'),
]
