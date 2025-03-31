from django.shortcuts import render

def home_view(request):
    """Displays the home page."""
    # You could add context here if the home page needs dynamic data later
    context = {}
    return render(request, 'pages/home.html', context)

def about_view(request):
    """Displays the about page."""
    # You could add context here if the about page needs dynamic data later
    context = {}
    return render(request, 'pages/about.html', context)

# Note: The actual content for these pages will come from the
# templates/pages/home.html and templates/pages/about.html files,
# which should be adapted from your existing index.html and about.html.
