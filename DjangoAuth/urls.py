from django.urls import path
from django.contrib.auth import views as auth_views

from authen import views

from django.conf.urls import include


urlpatterns = [
    path('', views.home, name='home'),
    # path('', include("reader.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile', auth_views.LoginView.as_view(template_name='auth/profile.html'), name='profile'),
    path('search-news', views.searchNews, name='search'),
]
