from django.urls import path
from . import views

app_name ='super_admin'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.registration, name='register'),
    path('univ/<str:id>/', views.institution_detail, name='univ'),
    path('account/', views.createAccount, name='account'),
    path('user_profile/', views.useProfile, name='user_profile'),
    path('update_unv/<int:pk>/',views.updateUnv, name='update_unv'),
    path('delete_unv/<int:pk>/',views.deleteUnv, name='delete_unv'),
    path('delete_user/<int:pk>/',views.deleteRegAdmin, name='delete_user'),
    path('activity_logs/', views.activity_logs, name='activity_logs'),
    path('view_request/', views.view_request, name='view_request'),
    path('approve_request/<str:id>/',views.approve_request, name='approve_request'),
    path('message_ra/<str:id>/',views.message_with_registrar_admin, name='message_ra'),
    path('check/', views.checker, name='check')
]