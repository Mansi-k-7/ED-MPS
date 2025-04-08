from django.urls import path

from user import views

urlpatterns = [
    path('Userregister', views.Userregister, name='Userregister'),
    path('userhome/', views.userhome, name='userhome'),
    path('UploadImageAction/', views.UploadImageAction, name='UploadImageAction'),
    path('UserLiveCameDetect/', views.UserLiveCameDetect, name='UserLiveCameDetect'),
    path('play_music/<str:emotion>/', views.play_music, name='play_music'),
    path('stop_music/', views.stop_music, name='stop_music'),
    path('userlogout/', views.userlogout, name='userlogout'),
]