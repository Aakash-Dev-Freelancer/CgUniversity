"""
URL configuration for CG_University project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from CG_International_University_App.sitemaps import AllPagesSitemap  # Replace with your actual app and sitemap

sitemaps = {
    'allpages': AllPagesSitemap,
}
urlpatterns = [
    path('google123456789abcdef.html', TemplateView.as_view(template_name="google123456789abcdef.html", content_type='text/html')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('admin/', admin.site.urls),
    path('', include('CG_International_University_App.urls')),
    path('cg_api/', include('cgapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
