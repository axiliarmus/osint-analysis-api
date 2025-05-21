from rest_framework import serializers
from .models import OSINTReport

class OSINTReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSINTReport
        fields = ['report_type', 'raw_data']
    
    def validate_raw_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("raw_data debe ser un objeto JSON válido.")
        return value