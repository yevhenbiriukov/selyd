# Generated by Django 4.0.4 on 2023-02-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0026_alter_product_social_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='banner',
            field=models.ImageField(blank=True, help_text='Банер категорії', null=True, upload_to='categories/banners/', verbose_name='Банер'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, help_text='Значок чого', null=True, upload_to='categories/images/', verbose_name='Значок'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='banner',
            field=models.ImageField(blank=True, help_text='Банер підкатегорії', null=True, upload_to='subcategories/banners/', verbose_name='Банер'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(blank=True, help_text='Значок підкатегорії', null=True, upload_to='subcategories/images/', verbose_name='Значок'),
        ),
    ]
