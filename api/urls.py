from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.GetRoutes.as_view()),
    path('projects/', views.GetProjects.as_view()),   
    path('projects/<str:pk>/', views.GetProject.as_view()),
    # jwt 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]