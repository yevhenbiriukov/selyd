from django.contrib.sitemaps import Sitemap
from .models import *

# При эксплуатации нужно будет в админке подставить реальный адрес для карты сайта
class ProductSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.9

    def items(self):

        return Product.objects.all()

    def lastmod(self, obj):

        return obj.created
