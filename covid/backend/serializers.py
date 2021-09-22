from .models import Covid
from rest_framework import serializers

class CovidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Covid
        fields = '__all__'

class MetricsSerializer(serializers.Serializer):
    total_cases = serializers.IntegerField()
    new_cases = serializers.IntegerField()
    recovered = serializers.IntegerField()
    tested = serializers.IntegerField()
    died = serializers.IntegerField()