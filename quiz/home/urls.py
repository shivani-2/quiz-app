from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('api/get-quiz/', views.get_quiz, name="get_quiz"),
    path('quiz/', views.quiz, name="quiz")


]