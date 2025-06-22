from .views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    CourseSubscribeAPIView,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    # Подписаться на курс
    path('courses/<int:course_id>/subscribe/', CourseSubscribeAPIView.as_view(), name='course-subscribe'),
    # Отписаться от курса
    path('courses/<int:course_id>/subscribe/', CourseSubscribeAPIView.as_view(), name='course-unsubscribe'),
     path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
     path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
 ]

