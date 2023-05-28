from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.index, name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]