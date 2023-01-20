from django import template
from ..models import *
from django.utils.safestring import mark_safe
import markdown
from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def total_products():
    return Product.objects.count()

@register.simple_tag
def get_categories():
    return Category.objects.filter(service_or_product='s')

@register.simple_tag
def get_logo():
    return Logo.objects.filter(pk=1)

@register.simple_tag
def get_footer_articles():
    return Article.objects.filter(footer_num__lt=10)

@register.simple_tag
def get_product_categories_banner():
    return Banner.objects.filter(name__icontains='product_categories')

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

######## default images and banners ########

@register.simple_tag
def get_default_banner():
    return Banner.objects.filter(name__icontains='default_banner')

@register.simple_tag
def get_default_image():
    return Image.objects.filter(name__icontains='default_image')

@register.simple_tag
def get_default_account_image():
    return Image.objects.filter(name__icontains='default_account')

@register.simple_tag
def get_default_product_image():
    return Image.objects.filter(name__icontains='default_product')

@register.simple_tag
def get_default_article_image():
    return Image.objects.filter(name__icontains='default_article')
