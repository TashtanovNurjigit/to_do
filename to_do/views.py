from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import (
    TaskListSerializer, TaskDetailSerializer, TaskValidateSerializer
)


class TaskListAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = TaskValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        task = Task.objects.create(
            title=data.get('title'),
            description=data.get('description')
        )
        return Response(data=TaskListSerializer(task, many=False).data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['id'])
        except Task.DoesNotExist:
            return Response(data={'error': 'Task not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        task.title = data.get('title')
        task.description = data.get('description')
        task.completed = data.get('completed')

        task.save()
        return Response(data=TaskDetailSerializer(task, many=False).data, status=status.HTTP_200_OK)
