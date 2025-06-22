from rest_framework import serializers
from .models import Course, Lesson, Subscription

class LessonSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'duration', 'order', 'user']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons       = LessonSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model  = Course
        fields = [
            'id', 'title', 'description',
            'lessons_count',
            'lessons',
            'user',
            'is_subscribed',
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    user   = serializers.ReadOnlyField(source='user.username')
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model  = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['id', 'user', 'course', 'created_at']