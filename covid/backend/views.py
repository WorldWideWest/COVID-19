import schedule as sc
import pandas as pd
import os

from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Covid
from .serializers import CovidSerializer

# Create your views here.

class CovidDataView(APIView):
    def get(self, request, format = None):
        covid_data = Covid.objects.all()
        serializer = CovidSerializer(covid_data, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = CovidSerializer(data = request.data, many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format = None):
        covid_data = Covid.objects.all()
        covid_data.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# Create scheduler to download the data and upload the data to sqlite db 


def job():
    path = os.path.join(settings.FILES_DIR, 'cleanData.xlsx')
    # url = "http://127.0.0.1:8000/api/"

    data = pd.read_excel(path, engine = "openpyxl")

    data['date'] = pd.to_datetime(data['date'], format = "%d.%m.%Y")
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')
    data['date'] = data['date'].astype(str)

    rowIter = data.iterrows()
    objects = [
        Covid(
            date = data['date'],
            total_cases = data['total_cases'],
            new_cases = data['new_cases'],
            population = data['population'],
            recovered = data['recovered'],
            tested = data['tested'],
            died = data['died']
        )
        for index, row in rowIter
    ]
    print(data.info())
    Covid.objects.all().delete()
    Covid.objects.bulk_create(objects)
