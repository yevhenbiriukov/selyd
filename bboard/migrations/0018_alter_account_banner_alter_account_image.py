# Generated by Django 4.0.4 on 2022-07-24 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0017_alter_account_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='banner',
            field=models.ImageField(blank=True, help_text="Банер для сторінки вашого проєкту (необов'язково)", null=True, upload_to='accounts/images', verbose_name='Банер'),
        ),
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, help_text="Логотип вашого проєкту (необов'язково)", null=True, upload_to='accounts/images/<django.db.models.fields.CharField>', verbose_name='Логотип'),
        ),
    ]
