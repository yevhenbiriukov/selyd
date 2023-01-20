from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    #list_display = ('name', 'tagline', 'city', 'status', 'prime_places', 'publish') #  список полей, которые мы хотим видеть
    # list_display_links = ('name', 'tagline',) # поля с гиперссылкой
    # list_editable = ('name', 'tagline',) # список полей кот будут редактируемы в админке
    #fields = ['name', 'city', ('tagline', 'publish')] # Атрибут полей перечисляет только те поля, которые должны отображаться в форме, по порядку. Поля отображаются по вертикали по умолчанию, но будут отображаться горизонтально, если вы дополнительно группируете их в кортеже
    # prepopulated_fields = {'slug': ('name',)} # предзаполнение полей
    #list_filter = ('name', 'tagline', 'city') # for right sidebar filter
    #search_fields = ('name', 'city') # for search bar at top
    #prepopulated_fields = {'name': ('name',)} # for prepopulating the key-field with the input of the field in value field (in tuple)
    #raw_id_fields = ('author',) # for displaying field with a lookup widget
    #date_hierarchy = 'created' # for navigation links below search bar
    #ordering = ('status', 'created') # for ordering columns by default
    
    # (!) В мозилла написано еще (последние два приема) как группировать поля + как показывать список связанных записей
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    #list_display = ('body', 'account', 'created', 'active')
    #list_filter = ('active', 'created', 'updated')
    #search_fields = ('name', 'email', 'body')
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_or_product', 'image', 'banner',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

class ArticleAdminForm(forms.ModelForm):
    summary = forms.CharField(label='Опис', widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = '__all__'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    pass
