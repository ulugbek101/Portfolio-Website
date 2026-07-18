from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News, Post


class EntrySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True          # emit one URL per language
    alternates = True    # with hreflang alternates
    model = None

    def items(self):
        return self.model.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class PostSitemap(EntrySitemap):
    model = Post


class NewsSitemap(EntrySitemap):
    model = News


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    i18n = True
    alternates = True

    def items(self):
        return ["index", "portfolio", "content:post_list", "content:news_list"]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "static": StaticSitemap,
    "posts": PostSitemap,
    "news": NewsSitemap,
}
