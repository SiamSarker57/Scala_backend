from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_package, name='analyze_package'),
    path('history/', views.get_analysis_history, name='history'),
    path('package/<int:package_id>/', views.get_package_details, name='package_details'),
    path('statistics/', views.get_statistics, name='statistics'),
]