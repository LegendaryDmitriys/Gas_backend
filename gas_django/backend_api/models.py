from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import request


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(request.data.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Brands(models.Model):
    id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand_name} ({self.country_of_origin})"


class Cars(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=6)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"


class Customers(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class FuelTypes(models.Model):
    fuel_type = models.CharField(max_length=25)
    octane_rating = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.fuel_type


class FuelColumns(models.Model):
    fuel = models.ForeignKey(FuelTypes, on_delete=models.CASCADE)
    column_number = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.fuel} - Column {self.column_number}"


class Fueling(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    fuel = models.ForeignKey(FuelTypes, on_delete=models.CASCADE)
    fuel_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fueling_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    column_number = models.ForeignKey(FuelColumns, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fueling {self.fueling_id} - {self.customer} - {self.fueling_date}"


class Products(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name


class StorePurchases(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.customer} - {self.purchase_date}"
