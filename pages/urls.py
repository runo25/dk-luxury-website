from django.urls import path
from . import views

app_name = 'pages' # Namespace for URLs

urlpatterns = [
    # The root URL ('/') is handled by the project-level urls.py,
    # which includes this file with an empty path prefix ('').
    path('', views.home_view, name='home'),      # Matches the root URL
    path('about/', views.about_view, name='about'), # Matches /about/
]
