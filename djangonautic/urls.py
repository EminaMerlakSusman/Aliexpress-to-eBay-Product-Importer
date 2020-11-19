from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('privacy_policy/', views.privacy_policy),
    path('', views.homepage),
    path('product_info/', views.product_info)
]

