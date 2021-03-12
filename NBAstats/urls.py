"""NBAstats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from NBAstatsApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog.as_view(), name="Inicio"),
    # path('partido/part&id=<int:id>&from=<str:from>&to=<str:to>/', views.match, name="Partido"),
    path('partido/full&team=<int:team>&day=<int:day>&month=<int:month>&year=<int:year>/', views.matchFull, name="PartidoEntero"),
    path('clasificacion/year=<int:year1>&<int:year2>/', views.ranking, name="Clasificacion"),
    path('posicion/team=<int:team>/', views.positions, name="Clasificacion"),
    path('equipo/team=<int:team>/', views.team, name="Equipo"),
    path('año/team=<int:team>&year=<int:year1>&<int:year2>/', views.year, name="Año"),
    path('mes/team=<int:team>&month=<int:month>&year=<int:year>/', views.month, name="Mes"),
    path('blog/', views.blog.as_view(), name="Blog"),
    path('blog/<int:id>/', views.blogDetail, name="Blog item"),
    path('versus/', views.versus, name="Versus"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
