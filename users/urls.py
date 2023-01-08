from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register_, name='register'),

    path('account/', views.useraccount, name='account'),
    path('edit-account/', views.edit_account, name='edit-account'),
    path('create-skill/', views.create_skill, name='create-skill'),
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.message, name='message'),
    path('send-message/<str:pk>/', views.create_message, name='create-message'),

    path('', views.profile, name='profile'),
    path('profile/<str:pk>/', views.userprofile, name='user-profile'),


]