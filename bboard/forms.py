from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, fields
from .models import *
from django import forms


class EmailProductForm(forms.Form):
    # name = forms.CharField(max_length=25)
    # email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        
        
class AccountForm(forms.ModelForm):
    # price = forms.DecimalField(label='Цeнa', decimal_places=2)
    # rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
    #     label='Рубрика', help_text='He забудьте задать рубрику!',
    #     widget=forms.widgets.Select(attrs={'size': 8}))
    
    summary = forms.CharField(widget = forms.widgets.Textarea(), 
        help_text='Описание такое')
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget = forms.widgets.Select(attrs={'size': 8}),
        empty_label='Город не выбран'
    )
    
    class Meta:
        model = Account
        fields = ['name', 'tagline', 'summary', 'tel', 'banner', 'image',]
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'account', 'banner',]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'summary', 'description', 'tags', 'availability_status',
                'category', 'subcategory', 'department', 'price', 'new_price', 'image',
                'banner', 'account']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.category_subcategories.order_by('name')
            pass
        
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор паролю', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))