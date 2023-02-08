from django.urls import path

from composter import views
from django.views.generic import RedirectView

app_name = 'composter'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('composter/', views.composter, name='composter'),
    path('input-entry/', views.InputFormView.as_view(), name='input_entry'),
    path('temp-entry/', views.temp_entry, name='temp_entry'),
    path('output-entry/', views.output_entry, name="output_entry"),
    path('restaurants/', views.restaurant_request_form, name='restaurant_form'),

    # admin only urls
    path('simple-admin/', views.simple_admin, name='simple_admin'),

]
