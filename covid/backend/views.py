from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import pandas as pd
import json

from .models import Covid
from .serializers import CovidSerializer, MetricsSerializer

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

class MetricsView(APIView):
    def get(self, request, format = None):
        dataFrame = pd.DataFrame(
            list(Covid.objects.all().values('total_cases', 'new_cases', 'recovered', 'tested', 'died')))
        corrFrame = dataFrame.corr().to_json(orient = "records")
        
        return Response(json.loads(corrFrame))


