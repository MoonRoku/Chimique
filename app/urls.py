from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pesquisar/', views.pesquisar_produto, name='pesquisar_produto'),
]