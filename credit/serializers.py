from rest_framework import serializers
from .models import CreditScoreResult

class CreditScoreResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScoreResult
        fields = '__all__'
