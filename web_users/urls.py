from django.urls import path
from. import views
app_name ='web_users'
urlpatterns = [
    path('', views.web_user, name='index'),
    path('search/', views.certificate,  name='search'),


]