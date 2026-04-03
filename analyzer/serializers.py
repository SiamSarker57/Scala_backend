from rest_framework import serializers
from .models import Package, AnalysisResult

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'version', 'ecosystem', 'created_at']

class AnalysisResultSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)
    
    class Meta:
        model = AnalysisResult
        fields = ['id', 'package', 'is_malicious', 'severity', 
                 'confidence_score', 'behavior_analysis', 
                 'alternative_suggestions', 'analyzed_at']