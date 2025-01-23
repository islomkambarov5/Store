from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('', views.ProductList.as_view(), name='productlist'),
    path('change_password/', views.PasswordChangeApiView.as_view(), name='change_password'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
]