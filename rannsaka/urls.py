"""rannsaka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from base.views.views import MyLoginView
from base.views.views import change_password

urlpatterns = [
    # Base app
    path('base/', include('base.urls')),
    # Admin
    path('admin/', admin.site.urls),
    # Authentication
    path('login/', MyLoginView.as_view(), name='login'),
    path('password/', change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
