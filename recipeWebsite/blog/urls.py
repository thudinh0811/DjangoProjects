from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    path('login/', views.Login, name = 'login'),
    path('auth/', views.Auth, name= 'auth'),
    path('logout/', views.log_out, name = 'logout'),
    path('register/', views.Register, name='register'),
    path('createuser/', views.create_user, name= 'createuser'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('profile/', views.ProfileView, name='profile'),
]