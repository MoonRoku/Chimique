from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pesquisar/', views.pesquisar_produto, name='pesquisar_produto'),
    path('registrar_produto/', views.registrar_produto, name='registrar_produto'),
]