from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from sermons.models import Sermon


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return (
            "home",
            "about",
            "how_we_are_led",
            "partner_with_us",
            "beliefs",
            "belief_detail:nicene-creed",
            "belief_detail:apostles-creed",
            "belief_detail:baptist-faith-and-message-2000",
            "confession",
            "new_here",
            "giving",
            "sermons:list",
        )

    def location(self, item):
        if item == "sermons:list":
            return reverse(item)
        if ":" in item:
            view_name, slug = item.split(":", 1)
            return reverse(view_name, kwargs={"slug": slug})
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
