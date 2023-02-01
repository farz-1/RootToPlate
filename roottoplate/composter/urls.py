from django.urls import path

from composter import views

app_name = 'composter'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('composter/', views.composter, name='composter'),
    path('input-entry/', views.input_entry, name='input_entry'),
    path('temp-entry/', views.temp_entry, name='temp_entry'),
    path('output-entry/', views.output_entry, name="output_entry"),
    path('restaurants/', views.restaurant_request_form, name='restaurant_form'),

    # admin only urls
    path('add-user/', views.add_user, name='add_user'),
    path('add-input-type/', views.add_input_type, name='add_input_type'),
    path('change-password/', views.change_password, name='change_password')
]
