from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from sermons.models import Sermon


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ("home", "about", "new_here", "giving", "sermons:list")

    def location(self, item):
        return reverse(item)


class SermonSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Sermon.objects.filter(is_published=True)

    def location(self, item):
        return reverse("sermons:detail", kwargs={"slug": item.slug})

    def lastmod(self, item):
        return item.updated_at
