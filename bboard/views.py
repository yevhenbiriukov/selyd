from typing import IO
from django.urls.base import reverse_lazy
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import views
# Импорты для аутентификации и регистрации
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


# В этих двух классах содержиться неплохой пример, как можно валидировать значения при регистрации:


# >>> Главная страница <<<
class CategoryListView(ListView):
    model = Category
    template_name = 'bboard/base.html'
    context_object_name = 'categories'
    # При наличии этого атрибута, будет отображаться вместо ошибки \
    # страница 404 с случаях: если ввести несущ слаг; если в get_context_data \
    # обращаемся к элементам, которых нет
    # Но, по факту, этот параметр выдает 404, когда у меня на главной нет записей для вывода
    allow_empty = True

    def get_queryset(self):
        return Category.objects.filter(service_or_product='s')

    def get_context_data(self, **kwargs):
        # отношение продукта к к-либо из привелегированных категорий можно мониторить/редактировать через фильты в админке. Нужно будет сделать это
        context = super(CategoryListView, self).get_context_data(**kwargs)
        # Головний баннер
        # i для анкоров баннеров в модели есть возможность указания проекта/продукта
        context['top_banners'] = (Banner.objects.filter(name__icontains='_top') & Banner.objects.filter(state='a'))[:1]
        # Топ-10 проєктів
        context['top_10_projects'] = Account.objects.filter(prime_places='1') & Account.objects.filter(state='a')
        # Популярні товари та послуги
        # ! Нужно будет как-то ограничить количество выводимых записей в этой категории
        # ! Для этой категии вообще нужно будет придумать какие помещать в нее товары
        context['products_popular'] = Product.objects.filter(prime_places='1')
        # Баннери у середині
        context['middle_banners'] = (Banner.objects.filter(name__icontains='_middle') & Banner.objects.filter(state='a'))[:2]
        # Нещодавно додані - перший стовбчик
        context['products_recent'] = Product.objects.order_by('-created')[:3]
        # Нещодавно додані - другий стовбчик
        context['products_recent2'] = Product.objects.order_by('-created')[3:6]
        # Кращий вибір - перший стовбчик
        context['products_best'] = Product.objects.filter(prime_places='3')[:3]
        # Кращий вибір - другий стовбчик
        context['products_best2'] = Product.objects.filter(prime_places='3')[3:6]
        # Топ переглядів - перший стовбчик
        # ! Cделать как-то для топ-просмотров отображение на основе реальной статистики
        context['products_top'] = Product.objects.filter(prime_places='4')[:3]
        # Топ переглядів - другий стовбчик
        context['products_top2'] = Product.objects.filter(prime_places='4')[3:6]
        return context


# >>> Страница категорий продуктов с типом Товар <<<
class ProductCategoriesListView(ListView):
    model = Category
    template_name = 'bboard/category/product_categories.html'
    context_object_name = 'product_categories'
    paginate_by = 20
    allow_empty = True

    def get_queryset(self):
        return Category.objects.filter(service_or_product='p')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoriesListView, self).get_context_data(**kwargs)
        context['banner'] = Banner.objects.filter(name='products_categories_page_banner')[:1] # эту запись нужно будет каким-то образом выделять среди остальных, чтобы случайно не удалить ее. Да, и находить ее нужно будет быстро
        return context


# >>> Страница подкатегорий определенной категории <<<
class CategorySubcategoriesListView(ListView):
    model = Subcategory
    template_name = 'bboard/subcategory/category_subcategories.html'
    context_object_name = 'subcategories'
    paginate_by = 20

    def get_queryset(self):
        return Subcategory.objects.filter(category=get_object_or_404(Category, pk=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context = super(CategorySubcategoriesListView, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        # Для лого использовать процессоры, чтобы не прописывать обращение в каждой вью
        return context


# >>> Страница продуктов в определенной категории <<<
# в каждую запись продукта сюда нужно будет вывести много разной информации - теги, цену и пр.
class SubcategoryProductListView(ListView):
    model = Product
    template_name = 'bboard/product/subcategory_products.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        # Добавить в фильтрацию те, которые Под заказ + во все другие контроллеры
        return Product.objects.filter(subcategory=get_object_or_404(Subcategory, pk=self.kwargs['pk']), availability_status='y')

    def get_context_data(self, **kwargs):
        context = super(SubcategoryProductListView, self).get_context_data(**kwargs)
        context['subcategory'] = get_object_or_404(Subcategory, pk=self.kwargs['pk'])
        return context


# >>> Страница продуктов с определенным тегом <<<
# Только нужно будет организовать добавление тега через форму создания продукта
class TagProductListView(ListView):
    model = Product
    template_name = 'bboard/product/subcategory_products.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Product.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super(TagProductListView, self).get_context_data(**kwargs)
        #context['subcategory'] = get_object_or_404(Subcategory, pk=self.kwargs['pk'])
        return context


# >>> Страница отдельно взятого продукта <<<
class ProductDetailView(DetailView):
    model = Product
    template_name = 'bboard/product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # Здесь уже нужно будет отобразить по-настоящему самые популярные продукты продавца
        # А, еще нужно исключить текущий продукт из списка внизу
        # Организовать цену товара по умолчанию - чтобы показывалось хоть что-то, но не None
        r = Product.objects.get(pk=self.kwargs['pk']).account
        context['products'] = r.account_products.all()[:4]
        return context


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'bboard/subcategory/subcategories_dropdown.html', {'subcategories': subcategories})


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'bboard/product/product_form.html'
    # success_url = reverse_lazy('product_categories') # Закомментил потому что не работало
    # login_url = reverse_lazy('home') # адрес перенаправления для незарегистрированного пользователя
    # raise_exeption = True # генерация страницы 403, если пользователь неавторизрован

    def form_valid(self, form):
        # В мозилла Джанго в задании diy есть хороший пример использования этого метода form_valid
        form.instance.project_owner = self.request.user
        return super(ProductCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = Account.objects.filter(account_owner=self.request.user)
        context['form'].fields['department'].queryset = Department.objects.filter(account_owner=self.request.user)
        return context


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'bboard/product/product_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None, **kwargs):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(Product, project_owner=self.user_id, pk=self.kwargs['pk'])
        
        # account_owner=self.user_id, 
    
    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = Account.objects.filter(account_owner=self.request.user)
        context['form'].fields['department'].queryset = Department.objects.filter(account_owner=self.request.user)
        return context


class AccountDetailView(DetailView):
    model = Account
    template_name = 'bboard/account/account_detail.html'
    paginate_by = 20
    #slug_url_kwarg = 'account'
    #context_object_name = 'account'
    
    def dispatch(self, request, *args, **kwargs):
        self.owner = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        # В скидках
        context['discount_products'] = Product.objects.filter(account=get_object_or_404(Account, pk=self.kwargs['pk'])) & Product.objects.filter(new_price__gt=0)
        # Просто все продукты
        context['products'] = Product.objects.filter(account=get_object_or_404(Account, pk=self.kwargs['pk']))
        # Отделы
        context['departments'] = Department.objects.filter(account=get_object_or_404(Account, pk=self.kwargs['pk']))
        # Новинки
        context['products_recent'] = Product.objects.filter(account=get_object_or_404(Account, pk=self.kwargs['pk'])).order_by('-created')[:3]
        context['products_recent2'] = Product.objects.filter(account=get_object_or_404(Account, pk=self.kwargs['pk'])).order_by('-created')[3:6]
        context['is_owner'] = context['account'].account_owner == self.owner
        context['is_products_reserve'] = context['account'].products_amount > context['account'].account_products.count()
        context['is_departments_reserve'] = context['account'].departments_amount > context['account'].account_departments.count()
        return context


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'tagline', 'summary', 'tel', 'city', 'banner', 'image',]
    template_name = 'bboard/account/account_form.html'
    
    def form_valid(self, form):
        form.instance.account_owner = self.request.user
        return super(AccountCreate, self).form_valid(form)

# Добавить возможность деактивации проекта
class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'tagline', 'summary', 'tel', 'city', 'banner', 'status', 'image',]
    template_name = 'bboard/account/account_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None, **kwargs):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(Account, account_owner=self.user_id, pk=self.kwargs['pk'])

# Настроить этот класс, чтобы сообщения могли оставлять только владелец проекта и админ
class MessageCreate(CreateView):
    model = Message
    fields = ['body',]
    template_name = 'bboard/account/comment_form.html'

    def get_success_url(self):
        return reverse('bboard:comment_create', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(MessageCreate, self).get_context_data(**kwargs)
        context['account'] = get_object_or_404(Account, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        #form.instance.author = self.request.user
        form.instance.account=get_object_or_404(Account, pk = self.kwargs['pk'])
        return super(MessageCreate, self).form_valid(form)


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'bboard/department/department_detail.html'
    paginate_by = 2
    
    def dispatch(self, request, *args, **kwargs):
        self.owner = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(department=get_object_or_404(Department, pk=self.kwargs['pk']))
        r = Department.objects.get(pk=self.kwargs['pk']).account
        context['departments'] = r.account_departments.all()
        context['is_owner'] = context['department'].account_owner == self.owner
        context['is_products_reserve'] = context['department'].account.products_amount > context['department'].account.account_products.count()
        return context


class DepartmentCreate(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['name', 'account', 'banner',]
    template_name = 'bboard/department/department_form.html'

    def form_valid(self, form):
        form.instance.account_owner = self.request.user
        return super(DepartmentCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentCreate, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = Account.objects.filter(account_owner=self.request.user)
        return context


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ['name', 'account', 'banner',]
    template_name = 'bboard/department/department_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Пробовать через этот метод передавать pk разных объектов в следующий контроллер
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None, **kwargs):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(Department, account_owner=self.user_id, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentUpdate, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = Account.objects.filter(account_owner=self.request.user)
        return context


# Добавить класс удаления отдела


class AccountListView(ListView):
    model = Account
    template_name = 'bboard/account/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        return context


class MyAccountListView(ListView):
    model = Account
    template_name = 'bboard/account/my_account_list.html'
    context_object_name = 'accounts'
    paginate_by = 20
    allow_empty = True
    
    def get_queryset(self):
        return Account.objects.filter(account_owner=self.request.user)


class ArticleListView(ListView):
    model = Article
    template_name = 'bboard/article/article_list.html'
    context_object_name = 'articles'
    paginate_by = 20


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'bboard/article/article_detail.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bboard/register_user.html'
    success_url = reverse_lazy('bboard:login_user')


from django.shortcuts import render
from .my_captcha import FormWithCaptcha
class LoginUser(LoginView):
    # Вместо этого метода можно использовать константу LOGIN_REDIRECT_URL в настройках - 
    # эффект будет тот же - перенаправление
    form_class = LoginUserForm
    template_name = 'bboard/login_user.html'
    
    def get_success_url(self):
        return reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['captcha'] = FormWithCaptcha
        return context

# Как еще можно использовать систему отправки по e-mail:
# - чтобы пользователи подавали заявки на участие в проекте. Только нужно будет ставить ограничение по отправленным сообщениям с одного устройства
# - чтобы пользователи могли пожаловаться на продукт (только по случаям нарушения законодательства на сайте). + То же, только для всего сайта в футере. Тоже нужна система ограничений
def product_share(request, pk):
    # Retrieve post by id
    product = get_object_or_404(Product, id=pk) # status='published'
    sent = False
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailProductForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            product_url = request.build_absolute_uri(product.get_absolute_url())
            subject = f"{cd['comments']} recommends you read " f"{product.name}"
            message = f"Read {product.name} at {product_url}\n\n" f"{cd['comments']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ivo.hrolf@gmail.com', [cd['to']])
            sent = True
    # ... send email
    else:
        cd = None
        form = EmailProductForm()
    return render(request, 'bboard/product/share.html', {'product': product, 'form': form, 'sent': sent, 'cd': cd})

# Систему комментов можно применить для чата с клиентом


# (!) заменить все методы get на те, которые не возвращают ошибку при отсутствии записи

# (!) переписать методы и шаблоны под возможность наличия разных логотипов (например, по величине разных). Т. е. чтобы можно было использовать на страницах вариации логотипа

# (!) перед релизом проверять работу страниц на БД без записей - не будет ли ошибок
