from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from .feeds import LatestAccountsFeed

app_name = 'bboard'

urlpatterns = [
    path('', CategoryListView.as_view(), name='index'),
    path('product_categories', ProductCategoriesListView.as_view(), name='product_categories'),
    path('category/<int:pk>/', CategorySubcategoriesListView.as_view(), \
        name='category-subcategories'),
    path('subcategory/<int:pk>/', SubcategoryProductListView.as_view(), \
        name='subcategory-products'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('tag/<slug:tag_slug>/', TagProductListView.as_view(), name='product_list_by_tag'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/update', ProductUpdate.as_view(), name='product_update'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('account/create/', AccountCreate.as_view(), name='account_create'),
    path('account/<int:pk>/update', AccountUpdate.as_view(), name='account_update'),
    path('account/<int:pk>/comment', MessageCreate.as_view(), name='comment_create'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('department/create/', DepartmentCreate.as_view(), name='department_create'),
    path('department/<int:pk>/update', DepartmentUpdate.as_view(), name='department_update'),
    path('accounts', AccountListView.as_view(), name='accounts'),
    path('articles', ArticleListView.as_view(), name='articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('my_accounts/', MyAccountListView.as_view(), name='my_accounts'),
    path('<int:pk>/share/', views.product_share, name='product_share'),
    path('feed/', LatestAccountsFeed(), name='account_feed'),
    path('3f42b97f4755040d05fa6491481f2e7644b9a9a198b8ff49/', RegisterUser.as_view(), name='register'),
    path('login_user/', LoginUser.as_view(), name='login_user'),
]
