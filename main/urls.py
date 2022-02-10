from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('delete/<str:pk>', views.delete, name='delete'),
    re_path(r'delete/(?P<pk>\d+)', views.delete, name='delete'),
    path('update/<str:type>/<str:stock>/<int:count>', views.update, name='update')
]