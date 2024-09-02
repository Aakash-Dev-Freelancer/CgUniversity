from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AllPagesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'contact', ...]  # Add all your URL names here

    def location(self, item):
        return reverse(item)
