from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input-entry/', views.input_entry, name='input_entry')
]
