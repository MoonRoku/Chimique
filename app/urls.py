from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pesquisar/', views.pesquisar_produto, name='pesquisar_produto'),
    path('registrar_produto/', views.registrar_produto, name='registrar_produto'),
    path('lista/', listaView.as_view(), name='lista'),
    path('delete/<int:id>/', deleteProduto.as_view(),name='delete'),
    path('misturar/', misturar_compostos, name='misturar_compostos'),
]