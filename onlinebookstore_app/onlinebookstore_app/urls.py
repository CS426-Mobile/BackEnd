from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('', include('Author.urls')),
    path('', include('Book.urls')),
    path('', include('Category.urls')),
    path('', include('CustomerCartBook.urls')),
    path('', include('CustomerFavorite.urls')),
    path('', include('CustomerFollow.urls')),
    path('', include('Order.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
]

# Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)