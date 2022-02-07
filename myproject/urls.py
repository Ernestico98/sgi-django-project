"""myproject URL Configuration

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
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from sgi import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('signup/extern/', views.signup_extern, name='signup_extern'),
    path('new_group/', views.new_group, name='new_group'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('new_room/', views.new_room, name='new_room'),
    path('new_resource/', views.new_resource, name='new_resource'),
    path('estado/', views.estado, name='estado'),
    path('estado/<grupo_pk>/', views.estado_por_grupo, name='estado_por_grupo'),
    path('valor_medios/', views.valor_medios, name='valor_medios'),
    path('prestamo/registro/', views.registrar_prestamo, name='registrar_prestamo'),
    path('prestamo/devolucion/', views.registrar_devolucion, name='registrar_devolucion'),
    path('prestamo/beneficiarios/', views.beneficiarios, name='beneficiarios'),
    path('prestamo/beneficiarios/<grupo_pk>/', views.beneficiarios_por_grupo, name='beneficiarios_por_grupo'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('prestamos/<grupo_pk>/', views.prestamos_por_grupo, name='prestamos_por_grupo'),
]
