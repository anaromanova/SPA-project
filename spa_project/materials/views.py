from rest_framework import viewsets, generics
from .models      import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import NotModeratorCannotModify, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        NotModeratorCannotModify,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        NotModeratorCannotModify,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        NotModeratorCannotModify,
        IsOwnerOrReadOnly,
    ]
