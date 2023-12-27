from rest_framework import serializers
from .models import CustomUser
from .models import Brands
from .models import Cars
from .models import Customers
from .models import FuelTypes
from .models import FuelColumns
from .models import Fueling
from .models import Products
from .models import StorePurchases

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'

class CarsSerializer(serializers.ModelSerializer):
    brand = BrandsSerializer()
    class Meta:
        model = Cars
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class FuelTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelTypes
        fields = '__all__'

class FuelColumnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelColumns
        fields = '__all__'


class FuelingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fueling
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class StorePurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePurchases
        fields = '__all__'