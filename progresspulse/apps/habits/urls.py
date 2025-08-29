from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('update/<int:pk>/', views.habit_update, name='habit_update'),
    path('delete/<int:pk>/', views.habit_delete, name='habit_delete'),
]