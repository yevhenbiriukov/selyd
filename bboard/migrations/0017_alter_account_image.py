# Generated by Django 4.0.4 on 2022-07-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0016_alter_account_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, help_text="Логотип вашого проєкту (необов'язково)", null=True, upload_to='accounts/images', verbose_name='Логотип'),
        ),
    ]
