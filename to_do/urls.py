from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('task/', TaskListAPIView.as_view()),
    path('task/<int:id>/', TaskDetailAPIView.as_view())
]
