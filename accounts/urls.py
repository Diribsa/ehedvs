from django.urls import path
from. import views


app_name ='accounts'
urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('404/', views.not_found, name='404'),
    path('me/', views.me, name='me'),
    
]