from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('', views.homepage),
    path('product_info/', views.product_info),
    path(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status')
]

