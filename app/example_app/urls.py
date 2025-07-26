"""
URL configuration for example_app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (
    TodoFormView, 
    ToggleTodoView, 
    DeleteTodoView, 
    TodoListView,
    DashboardView,
    todo_stats_api,
    bulk_action_api
)

app_name = 'example_app'

urlpatterns = [
    path('', TodoFormView.as_view(), name='todo_form'),
    path('list/', TodoListView.as_view(), name='todo_list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/toggle/', ToggleTodoView.as_view(), name='toggle_todo'),
    path('<int:pk>/delete/', DeleteTodoView.as_view(), name='delete_todo'),
    
    # API endpoints
    path('api/stats/', todo_stats_api, name='todo_stats_api'),
    path('api/bulk-action/', bulk_action_api, name='bulk_action_api'),
]
