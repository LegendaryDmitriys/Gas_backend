# Generated by Django 5.0 on 2023-12-25 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('country_of_origin', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FuelColumns',
            fields=[
                ('column_number', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='FuelTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_type', models.CharField(max_length=25)),
                ('octane_rating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('year', models.PositiveIntegerField()),
                ('registration_number', models.CharField(max_length=6)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.brands')),
            ],
        ),
        migrations.CreateModel(
            name='Fueling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fueling_date', models.DateField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.cars')),
                ('column_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.fuelcolumns')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.customers')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.fueltypes')),
            ],
        ),
        migrations.AddField(
            model_name='Fuelcolumns',
            name='fuel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.fueltypes'),
        ),
        migrations.CreateModel(
            name='StorePurchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField()),
                ('product_quantity', models.IntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.customers')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.products')),
            ],
        ),
    ]
