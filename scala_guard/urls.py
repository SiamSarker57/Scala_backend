from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('analyzer.urls')),
]

def home(request):
    return HttpResponse("""
        <h1>Welcome to Scala-Guard API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/admin/">/admin/</a> - Admin Panel</li>
            <li><a href="/api/history/">/api/history/</a> - Analysis History</li>
            <li><a href="/api/statistics/">/api/statistics/</a> - Statistics</li>
        </ul>
        <p>Use POST request to /api/analyze/ for package analysis</p>
    """)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('analyzer.urls')),
]
