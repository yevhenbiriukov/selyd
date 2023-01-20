from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import *

class LatestAccountsFeed(Feed):
    title = 'My bboard'
    link = reverse_lazy('bboard:accounts')
    description = 'New accounts of my bboard.'
    
    def items(self):
        return Account.objects.all()[:5]
    
    def item_title(self, item):
        return item.name
    
    def item_description(self, item):
        return truncatewords(item.summary, 30)
