# Generated by Django 5.0 on 2023-12-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0002_brands_customers_fuelcolumns_fueltypes_products_cars_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='car_images/'),
        ),
    ]