# Generated by Django 4.0.4 on 2022-07-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0012_alter_department_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='banner',
            field=models.ImageField(blank=True, default='default.jpg', help_text="Банер для сторінки вашого проєкту (необов'язково)", null=True, upload_to='', verbose_name='Банер'),
        ),
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', help_text="Логотип вашого проєкту (необов'язково)", null=True, upload_to='', verbose_name='Логотип'),
        ),
    ]
