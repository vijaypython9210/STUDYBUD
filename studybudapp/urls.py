from django.urls import path

from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-Room/',views.createRoom,name="create_room"),
    path('update-Room/<str:pk>',views.updateRoom,name="update_room"),
    path('delete-Room/<str:pk>',views.deleteRoom,name="delete_room"),
    path('follow/<str:pk>',views.follow,name='follow'),

    path('delete-message/<str:pk>',views.deleteMessage,name="delete_message"),

    path('user_profile/<str:pk>',views.userProfile,name="user_profile"),
    
    path('loginpage',views.loginpage,name="loginpage"),
    path('logout',views.logoutpage,name="logout"),
    path('register',views.registerpage,name="registerpage"),
]
