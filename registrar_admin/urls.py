from django.urls import path
from.import views
app_name = 'registrar_admin'
urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('faculty/',views.faculty, name='faculty'),
    path('program/', views.program, name='program'),
    path('delete_faculty/<str:id>/',views.delete_faculty, name='delete_faculty'),
    path('update_faculty/<str:id>/',views.update_faculty, name='update_faculty'),
    path('update_program/<str:id>/',views.update_program, name='update_program'),
    path('delete_program/<str:id>/',views.delete_program, name='delete_program'),
    path('account/', views.createAccount, name='account'),
    path('user_profile/', views.useProfile, name='user_profile'),
    path('delete_staff/<str:id>/',views.deleteRegStaff, name='delete_staff'),
    path('send_request/', views.send_request, name='send_request'),
    path('delete_request/<int:id>/', views.delete_request, name='delete_request'),
    path('activity_logs/', views.activity_logs, name='activity_logs'),
    path('certificate_archive/', views.certificate_archive, name='certificate_archive'),
    path('status_detail/<path:id>/', views.status_detail, name='status_detail' ),


]