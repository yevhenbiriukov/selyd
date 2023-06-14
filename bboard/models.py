from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
import numbers

######## Зробити на новій базі даних ########
# Завантажити дефолтні зображення
# Додати запис міста Вінницька область /


class City(models.Model):
    """Місто"""
    # i Порядок объявления полей влияет на порядок отображения полей в форме (но, можно и переопределить)
    name = models.CharField(
        help_text='Місто',
        max_length=200,
        # i Отображаемое имя поля
        verbose_name='Місто')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'


class Account(models.Model):
    """Проєкт"""
    account_owner = models.ForeignKey(
        User,
        help_text='Автор проєкту',
        null=True,
        # i Using CASCADE, you specify that when the referenced user is deleted, the database will also delete all related accounts.
        on_delete=models.SET_NULL,
        # i You specify the name of the reverse relationship, from User to Account, with the related_name attribute. This will allow you to access related objects easily.
        related_name='owner_accounts',
        verbose_name='Автор')
    name = models.CharField(
        help_text='Назва вашого проєкту',
        max_length=100,
        verbose_name='Назва')
    tagline = models.CharField(
        blank=True,
        default = 'Краще для вас',
        help_text='Слоган вашого проєкту (необов\'язково)',
        max_length=200,
        null=True,
        verbose_name='Слоган')
    summary = models.TextField(
        blank=True,
        default = 'Товар/послуга створена для вас',
        help_text='Опис товара/послуги, що пропонуєте (необов\'язково)',
        max_length=3000,
        null=True,
        verbose_name='Опис')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Змінено')
    tel = models.CharField(
        
        blank=True,
        help_text='Ваш робочий телефон (якщо хочете, щоб споживачі могли дзвонити вам)',
        max_length=200,
        null=True,
        verbose_name='Телефон')
    city = models.ForeignKey(
        City,
        blank=True,
        help_text='Місто, у якому продаєте товари або надаєте послуги (необов\'язково)',
        null=True,
        on_delete=models.SET_NULL,
        related_name='city_accounts',
        verbose_name='Місто')
    # i Когда нужно будет объявлять поле для CDN в другом формате, то можно будет иметь два варианта поля - закомментированное и актуальное
    banner = models.ImageField(
        blank=True,
        help_text='Банер для сторінки вашого проєкту (необов\'язково)',
        null=True,
        upload_to='accounts/banners/%Y/%m/',
        verbose_name='Банер')
    image = models.ImageField(
        blank=True,
        help_text='Логотип вашого проєкту (необов\'язково)',
        null=True,
        # upload_to='selyd/', upload_to='users/%Y/%m/%d/',
        upload_to='accounts/images/%Y/%m/',
        verbose_name='Логотип')
    products_amount = models.IntegerField(
        default = 10,
        help_text='Максимальна кількість продуктів',
        verbose_name="Кількість продуктів")
    departments_amount = models.IntegerField(
        default = 3,
        help_text='Максимальна кількість відділів',
        verbose_name="Кількість відділів")
    STATUS_CHOICES = (
        ('g', 'Gold'),
        ('s', 'Silver'),
        ('b', 'Bronze'),
        ('x', 'Blacklist'),)
    status = models.CharField(
        blank=True,
        choices=STATUS_CHOICES,
        default='s',
        help_text='Статус',
        max_length=1,
        verbose_name='Статус')
    STATE_CHOICES = (
        ('a', 'Active'),
        ('u', 'Unactive'),)
    state = models.CharField(
        blank=True,
        choices=STATE_CHOICES,
        default='u',
        help_text='Стан',
        max_length=1,
        verbose_name='Стан')
    PRIME_PLACES_CHOICES = (
        ('0', 'None'),
        ('1', 'Top-10'),)
    prime_places = models.CharField(
        
        blank=True,
        choices=PRIME_PLACES_CHOICES,
        default='0',
        help_text='Прайм-місце',
        max_length=1,
        verbose_name='Прайм-місце')

    class Meta:
        ordering = ['name', '-created']
        verbose_name = 'Проєкт' # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Проєкти' # Название модели в множественном числе
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bboard:account-detail', args=[str(self.id),])

class Message(models.Model):
    """Повідомлення"""
    
    project = models.ForeignKey(Account,
        on_delete=models.CASCADE,
        related_name='project_comments',
        verbose_name='Проєкт')
    body = models.TextField(max_length=500, verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    #updated = models.DateTimeField(auto_now=True)
    #active = models.BooleanField(default=True)
    #name = models.CharField(max_length=80)
    #email = models.EmailField()
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        
    def __str__(self):
        return f'Comment by __ on {self.account}'


class Category(models.Model):
    """Категорія"""
    # для имени категории желательно будет сделать slug, чтобы в url было читаемое имя. Но, это также вопрос возможности вытягивания во вьюхе всех связанных сущностей
    name = models.CharField(
        help_text='Категорія товарів/послуг',
        max_length=100,
        verbose_name='Назва')
    SERVICE_OR_PRODUCT_CHOICES = (
        ('s', 'Послуги'),
        ('p', 'Товари'),)
    service_or_product = models.CharField(
        choices=SERVICE_OR_PRODUCT_CHOICES,
        default='s',
        help_text='Категорія чого',
        max_length=1,
        verbose_name='Категорія чого')
    image = models.ImageField(
        blank=True,
        help_text='Значок чого',
        null=True,
        upload_to='categories/images/',
        verbose_name='Значок')
    banner = models.ImageField(
        blank=True,
        help_text='Банер категорії',
        null=True,
        upload_to='categories/banners/',
        verbose_name='Банер')

    class Meta:
        ordering = ['name'] # для пагинации сортировка должна быть включена
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name
    
    # ? Добавить get_absolute_url


class Subcategory(models.Model):
    """Підкатегорія"""
    name = models.CharField(
        help_text='Підкатегорія товарів/послуг',
        max_length=100,
        verbose_name='Підкатегорія')
    category = models.ForeignKey(
        Category,
        help_text='Категорія для поточної підкатегорії',
        null=True,
        on_delete=models.SET_NULL,
        related_name='category_subcategories',
        verbose_name='Категорія')
    image = models.ImageField(
        blank=True,
        help_text='Значок підкатегорії',
        null=True,
        upload_to='subcategories/images/',
        verbose_name='Значок')
    banner = models.ImageField(
        blank=True,
        help_text='Банер підкатегорії',
        null=True,
        upload_to='subcategories/banners/',
        verbose_name='Банер')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'
        
    # ? Добавить get_absolute_url


class Department(models.Model):
    """Відділ"""
    account_owner = models.ForeignKey(User,
        help_text='Автор проєкту',
        null=True,
        on_delete=models.SET_NULL,
        related_name='user_departments',
        verbose_name='Автор')
    name = models.CharField(
        help_text='Назва відділу проєкту. Наприклад, "Хлібобулочні вироби"',
        max_length=100,
        verbose_name='Відділ')
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name = 'account_departments',
        verbose_name='Проєкт')
    banner = models.ImageField(
        blank=True,
        help_text='Банер відділу',
        null=True,
        upload_to='departments/banners/%Y/%m/',
        verbose_name='Банер')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Відділ'
        verbose_name_plural = 'Відділи'
    
    def get_absolute_url(self):
        return reverse('bboard:department-detail', args=[str(self.id)])


class Product(models.Model):
    """Продукт"""
    project_owner = models.ForeignKey(
        User,
        help_text='Автор проєкту',
        null=True,
        on_delete=models.SET_NULL,
        related_name='owner_products',
        verbose_name='Автор')
    name = models.CharField(
        help_text='Назва товару чи послуги. Наприклад, "Хліб"',
        max_length=100,
        verbose_name='Назва')
    summary = models.TextField(
        blank=True,
        help_text='Опис товару/прослуги (необов\'язково)',
        max_length=1000,
        null=True,
        verbose_name='Опис')
    description = models.TextField(
        blank=True,
        help_text='Додаткові відомості про товар/послугу (необов\'язково)',
        max_length=3000,
        null=True,
        verbose_name='Додаткові відомості')
    social_links = models.TextField(
        blank=True,
        help_text='Посилання на соцмережі (необов\'язково). Пиши посилання через пробіл, наприклад: https://www.instagram.com/yevhenchlothar/ https://www.facebook.com/yevhen.chlothar',
        max_length=300,
        null=True,
        verbose_name='Посилання')
    tags = TaggableManager(
    #     # ! почему-то не работает с тегами на русском
    #     # сюда нужно будет прикрутить человекопонятные описания для вывода на странице
        blank=True,)
    AVAILABILITY_STATUS_CHOICES = (
        ('y', 'Так'),
        ('n', 'Ні'),
        ('o', 'Під заказ / За записом'),)
    availability_status = models.CharField(
        choices=AVAILABILITY_STATUS_CHOICES,
        default='y',
        help_text='Оберіть, чи доступний товар/послуга. Якщо обрати "Ні" - товар/послуга не буде відображатися споживачам',
        # реализовать это в контроллере
        max_length=1,
        verbose_name='Наявність')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Створено')
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Змінено')
    category = models.ForeignKey(Category,
        help_text='Оберіть категорію',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категорія')
    subcategory = models.ForeignKey(Subcategory,
        help_text='Оберіть підкатегорію',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Підкатегорія')
    department = models.ForeignKey(Department,
        blank=True,
        help_text='Оберіть відділ вашого продукту',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Відділ')
    price = models.DecimalField(
        blank=True,
        decimal_places=2,
        # default = 1,
        help_text='Вкажіть ціну (необов\'язково). Якщо не вказувати, то буде відображатися, значення "Договірна"', # сделать оборажение Договорная
        max_digits=8,
        null=True,
        verbose_name="Ціна")
    new_price = models.DecimalField(
        blank=True,
        decimal_places=2,
        # default = 1,
        help_text="Вкажіть нову ціну з урахуванням знижки (необов\'язково)",
        max_digits=8,
        null=True,
        verbose_name='Нова ціна')
    image = models.ImageField(
        blank=True,
        # default='product_image_default.jpg',
        help_text='Основна світлина продукту (необов\'язково)',
        null=True,
        upload_to='products/images/%Y/%m/',
        verbose_name='Світлина')
    #     # Сделать возможность добавления дополнительных фото + при их наличии - отображение на странице товара
    # image = CloudinaryField(
    #     blank=True,
    #     null=True,
    # )
    banner = models.ImageField(
        blank=True,
        # default='product_banner_default.jpg',
        help_text='Банер продукту (необов\'язково)',
        null=True,
        upload_to='products/banners/%Y/%m/',
        verbose_name='Банер')
    PRIME_PLACES_CHOICES = (
        ('0', 'None'),
        ('1', 'Popular'),
        ('3', 'Best'),
        ('4', 'Top'),)
    prime_places = models.CharField(
        blank=True,
        choices=PRIME_PLACES_CHOICES,
        default='0',
        help_text='Статус',
        max_length=1,
        verbose_name='Прайм-місце')
    account = models.ForeignKey(
        # должна быть связь с юзером/предприятием для поля account
        Account,
        help_text='Проєкт',
        null=True,
        on_delete=models.CASCADE,
        related_name='account_products',
        verbose_name='Проєкт')
    
    def social_links_output(self):
        if self.social_links: return self.social_links.split()
        else: return False
    
    def is_price(self):
        if isinstance(self.price, numbers.Number):
            if self.price > 0: return True
            else: return False
        else: return False
        
    def is_discount(self):
        if isinstance(self.new_price, numbers.Number):
            if self.new_price > 0: return True
            else: return False
        else: return False
    
    def discount_val(self):
        if self.new_price > 0:
            discount_val = int((1 - (self.new_price) / (self.price))*100)
            return discount_val
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
    
    def get_absolute_url(self):
        return reverse('bboard:product-detail', args=[str(self.id)])
    
    


class Article(models.Model):
    name = models.CharField(
        help_text='Назва статті',
        max_length=100,
        verbose_name='Назва')
    summary = models.TextField(
        blank=True,
        help_text="Текст статті",
        max_length=5000,
        null=True,
        verbose_name='Текст')
    description = models.TextField(
        blank=True,
        help_text="Додаткові відомості про статтю",
        max_length=3000,
        null=True,
        verbose_name='Додатково')
    image = models.ImageField(
        blank=True,
        help_text='Основна світлина статті',
        null=True,
        upload_to='articles/images/%Y/%m/',
        verbose_name='Світлина')
    banner = models.ImageField(
        blank=True,
        help_text='Основний банер статті',
        null=True,
        upload_to='articles/banners/%Y/%m/',
        verbose_name='Банер')
    FOR_WHOM_CHOICES = (
        ('p', 'Автори проєктів'),
        ('a', 'Всі'),
    )
    for_whom = models.CharField(
        choices=FOR_WHOM_CHOICES,
        default='p',
        help_text='Хто може бачити статтю',
        max_length=1,
        verbose_name='Видимість')
    footer_num = models.CharField(
        default='1',
        help_text='Номер статті у футері',
        max_length=2,
        verbose_name='Номер')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
        
    def get_absolute_url(self):
        return reverse('bboard:article-detail', args=[str(self.id),])


class Banner(models.Model):
    """Банер"""
    
    name = models.CharField(
        # пока имя будет содаваться вручную введением даты времени + суффикс
        help_text='Назва банеру',
        max_length=100,
        verbose_name='Назва')
    image = models.ImageField(
        help_text='Світлина банеру',
        upload_to='banners/images/%Y/%m/',
        verbose_name='Світлина')
    text_1 = models.CharField(blank=True, help_text='Текст №1 банеру',
        max_length=200, null=True, verbose_name='Текст №1')
    text_2 = models.CharField(blank=True, help_text='Текст №2 банеру',
        max_length=200, null=True, verbose_name='Текст №2')
    text_3 = models.CharField(blank=True, help_text='Текст №3 банеру',
        max_length=200, null=True, verbose_name='Текст №3')
    text_4 = models.CharField(blank=True, help_text='Текст №4 банеру',
        max_length=200, null=True, verbose_name='Текст №4')
    text_5 = models.CharField(blank=True, help_text='Текст №5 банеру',
        max_length=200, null=True, verbose_name='Текст №5')
    STATE_CHOICES = (
        ('a', 'Active'),
        ('u', 'Unactive'),)
    state = models.CharField(
        blank=True,
        choices=STATE_CHOICES,
        default='u',
        help_text='Стан',
        max_length=1,
        verbose_name='Стан')
    account = models.ForeignKey(Account,
        blank=True,
        help_text='Проєкт',
        null=True,
        on_delete=models.CASCADE,
        related_name='account_banners',
        verbose_name='Проєкт')
    product = models.ForeignKey(
        Product,
        blank=True,
        help_text='Продукт',
        null=True,
        on_delete=models.CASCADE,
        related_name='product_banners',
        verbose_name='Продукт')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Змінено')
    # в админке нужно будет сделать сортировку по Изменено
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['updated']
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'


class Logo(models.Model):
    """Логотип сайту"""
    name = models.CharField(
        help_text='Назва логотипу',
        max_length=100,
        verbose_name='Назва')
    image = models.ImageField(
        blank=True,
        help_text='Логотип сайту',
        upload_to='logos/images/',
        verbose_name='Логотип сайту')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Логотип'
        verbose_name_plural = 'Логотипи'


class Image(models.Model):
    """Світлина"""
    name = models.CharField(
        help_text='Назва світлини',
        max_length=100,
        verbose_name='Назва')
    image = models.ImageField(
        help_text='Світлина',
        upload_to='images/images/%Y/%m/',
        verbose_name='Світлина')
    text_1 = models.CharField(blank=True, help_text='Текст №1 світлини',
        max_length=200, null=True, verbose_name='Текст №1')
    STATE_CHOICES = (
        ('a', 'Active'),
        ('u', 'Unactive'),)
    state = models.CharField(
        blank=True,
        choices=STATE_CHOICES,
        default='u',
        help_text='Стан',
        max_length=1,
        verbose_name='Стан')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Змінено')
    # в админке нужно будет сделать сортировку по Изменено
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['updated']
        verbose_name = 'Світлина'
        verbose_name_plural = 'Світлини'


######## Сделать  ########


# Не сделано из Меле
# 11 slug = models.SlugField(max_length=250, unique_for_date='publish')
# 11 publish = models.DateTimeField(default=timezone.now,)
