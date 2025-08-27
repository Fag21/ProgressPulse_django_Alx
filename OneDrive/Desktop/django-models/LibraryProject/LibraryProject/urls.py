# project/urls.py

from django.contrib import admin
from django.urls import path, include  # Make sure to include 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),  # Existing URL for the admin interface

    # Include URLs from the 'relationship_app' app
    path('relationship_app/', include('relationship_app.urls')),  # Add this line
]
