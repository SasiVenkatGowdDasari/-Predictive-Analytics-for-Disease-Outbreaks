"""
URL configuration for Predictive_Analytics_for_Disease_Outbreaks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home),
    path('predict/',views.Predict),
    path('predict/result/',views.Result),
    # path('predict/',views.Predict),
    # path('result/?n1=&n2=&n3=&n4=&n5=&n6=',views.Result),
# views.___   here file name should be same of the function name in the views page
]
