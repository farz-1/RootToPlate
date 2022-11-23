from django.urls import path
from composter import views

app_name='composter'
urlpatterns=[
    path('',views.index,name='index'),
]