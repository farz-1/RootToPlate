from django.urls import path

from composter import views

app_name = 'composter'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('composter/', views.composter, name='composter'),
    path('input-entry/', views.input_entry, name='input_entry')
]
