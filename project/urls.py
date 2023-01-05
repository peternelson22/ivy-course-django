from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('create/', views.createproject, name='create'),
    
    path('project/<str:pk>/', views.project, name='project'),
    path('edit/<str:pk>/', views.updateproject, name='update'),
    path('delete/<str:pk>/', views.deleteproject, name='delete'),
]