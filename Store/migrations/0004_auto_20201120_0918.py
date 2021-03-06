# Generated by Django 3.1.1 on 2020-11-20 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products'),
        ),
    ]
