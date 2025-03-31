from django.urls import path
from . import views

app_name = 'contact' # Namespace for URLs

urlpatterns = [
    path('', views.contact_view, name='contact_form'), # URL for the contact page/form
]
