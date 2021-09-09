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
