from django.urls import path

from . import views
from django.conf.urls import url,include

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
]