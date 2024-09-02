from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from CG_International_University_App.sitemaps import AllPagesSitemap 

# Define sitemaps
sitemaps = {
    'allpages': AllPagesSitemap,
}

urlpatterns = [
    path('google123456789abcdef.html', TemplateView.as_view(
        template_name="google123456789abcdef.html", content_type='text/html')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('admin/', admin.site.urls),

    path('', include('CG_International_University_App.urls')),

    path('api/', include('cgapp.urls')),
] 

# Serve static and media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
