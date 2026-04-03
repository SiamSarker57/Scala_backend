from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Package, AnalysisResult
from .serializers import AnalysisResultSerializer
from .utils import analyze_package_security, get_package_info

@api_view(['POST'])
def analyze_package(request):
    data = request.data
    package_name = data.get('package_name')
    package_version = data.get('package_version', 'latest')
    ecosystem = data.get('ecosystem', 'npm')
    
    if not package_name:
        return Response({'error': 'Package name is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create package
    package, _ = Package.objects.get_or_create(
        name=package_name,
        version=package_version,
        ecosystem=ecosystem
    )
    
    # Get package info and analyze
    package_info = get_package_info(package_name, ecosystem)
    analysis_result = analyze_package_security(package_name, package_info)
    
    # Save analysis
    analysis = AnalysisResult.objects.create(
        package=package,
        is_malicious=analysis_result['is_malicious'],
        severity=analysis_result['severity'],
        confidence_score=analysis_result['confidence'],
        behavior_analysis=package_info,
        alternative_suggestions=analysis_result['alternatives']
    )
    
    serializer = AnalysisResultSerializer(analysis)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_analysis_history(request):
    analyses = AnalysisResult.objects.all()[:50]
    serializer = AnalysisResultSerializer(analyses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_package_details(request, package_id):
    try:
        analysis = AnalysisResult.objects.get(id=package_id)
        serializer = AnalysisResultSerializer(analysis)
        return Response(serializer.data)
    except AnalysisResult.DoesNotExist:
        return Response({'error': 'Analysis not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_statistics(request):
    total = AnalysisResult.objects.count()
    malicious = AnalysisResult.objects.filter(is_malicious=True).count()
    
    return Response({
        'total_scans': total,
        'malicious_count': malicious,
        'safe_percentage': ((total - malicious) / total * 100) if total > 0 else 100,
        'severity_counts': {
            'safe': AnalysisResult.objects.filter(severity='safe').count(),
            'low': AnalysisResult.objects.filter(severity='low').count(),
            'medium': AnalysisResult.objects.filter(severity='medium').count(),
            'high': AnalysisResult.objects.filter(severity='high').count(),
            'critical': AnalysisResult.objects.filter(severity='critical').count(),
        }
    })