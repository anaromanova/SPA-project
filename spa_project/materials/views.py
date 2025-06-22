from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models      import Course, Lesson, Subscription
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import NotModeratorCannotModify, IsOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .pagination  import StandardResultsSetPagination

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        NotModeratorCannotModify,
        IsOwnerOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination

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
    pagination_class = StandardResultsSetPagination

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


class CourseSubscribeAPIView(generics.GenericAPIView):
    """
    POST  /api/courses/<course_id>/subscribe/  → подписаться
    DELETE /api/courses/<course_id>/subscribe/ → отписаться
    """
    serializer_class   = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course = generics.get_object_or_404(Course, pk=kwargs['course_id'])
        sub, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )
        if not created:
            return Response(
                {'detail': 'Вы уже подписаны на этот курс.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.get_serializer(sub).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        course = generics.get_object_or_404(Course, pk=kwargs['course_id'])
        deleted, _ = Subscription.objects.filter(
            user=request.user,
            course=course
        ).delete()
        if not deleted:
            return Response(
                {'detail': 'Подписка на этот курс не найдена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)