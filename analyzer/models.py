from django.db import models
from django.utils import timezone

class Package(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    ecosystem = models.CharField(max_length=50, choices=[
        ('npm', 'npm'), ('pypi', 'PyPI'), ('maven', 'Maven'), ('rubygems', 'RubyGems')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}@{self.version}"

class AnalysisResult(models.Model):
    SEVERITY_CHOICES = [
        ('safe', 'Safe'), ('low', 'Low Risk'), ('medium', 'Medium Risk'),
        ('high', 'High Risk'), ('critical', 'Critical Risk'),
    ]
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='analyses')
    is_malicious = models.BooleanField(default=False)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='safe')
    confidence_score = models.FloatField(default=0.0)
    behavior_analysis = models.JSONField(default=dict)
    alternative_suggestions = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-analyzed_at']