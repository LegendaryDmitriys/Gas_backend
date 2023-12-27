import os
from django.conf import settings
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook
from django.apps import apps
import pandas as pd
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth import login as django_login
from django.db import IntegrityError

from .models import Brands
from .serializers import BrandsSerializer
from .models import Cars
from .serializers import CarsSerializer
from .models import Customers
from .serializers import CustomersSerializer
from .models import FuelTypes
from .serializers import FuelTypesSerializer
from .models import FuelColumns
from .serializers import FuelColumnsSerializer
from .models import Fueling
from .serializers import FuelingSerializer
from .models import Products
from .serializers import ProductsSerializer
from .models import StorePurchases
from .serializers import StorePurchasesSerializer



@api_view(['POST'])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response({'message': 'Пользователь успешно зарегистрирован'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    print(user)
    if user:
        login(request, user)
        return Response({'message': 'Вход выполнен успешно'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

class BrandsView(generics.ListCreateAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer

class CarsView(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer


class CustomersView(generics.ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer


class FuelTypesView(generics.ListCreateAPIView):
    queryset = FuelTypes.objects.all()
    serializer_class = FuelTypesSerializer

class FuelColumnsView(generics.ListCreateAPIView):
    queryset = FuelColumns.objects.all()
    serializer_class = FuelColumnsSerializer

class FuelingView(generics.ListCreateAPIView):
    queryset = Fueling.objects.all()
    serializer_class = FuelingSerializer

class ProductsView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class StorePurchasesView(generics.ListCreateAPIView):
    queryset = StorePurchases.objects.all()
    serializer_class = StorePurchasesSerializer

@csrf_exempt
def import_data(request):
    if request.method == "POST" and request.FILES.get("file") and request.POST.get("table_name"):
        file = request.FILES["file"]
        table_name = request.POST["table_name"]

        try:
            model_class = apps.get_model(app_label='backend_api', model_name=table_name)

            df = pd.read_excel(file)

            model_class.objects.all().delete()

            for index, row in df.iterrows():
                model_instance = model_class()
                for field_name in model_class._meta.fields:
                    if field_name.name == 'brand':
                        brand_id = row[field_name.name]
                        brand_instance = Brands.objects.get(id=brand_id)
                        setattr(model_instance, field_name.name, brand_instance)
                    else:
                        setattr(model_instance, field_name.name, row[field_name.name])
                model_instance.save()

            return JsonResponse({"message": "Данные успешно импортированы"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Некорректный запрос"}, status=400)

class CarDetailView(RetrieveAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FuelingDetailView(RetrieveAPIView):
    queryset = Fueling.objects.all()
    serializer_class = FuelingSerializer
    lookup_field = 'id'

class CustomersDetailView(RetrieveAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    lookup_field = 'id'

class TypeFuelsDetailView(RetrieveAPIView):
    queryset = FuelTypes.objects.all()
    serializer_class = FuelTypesSerializer
    lookup_field = 'id'