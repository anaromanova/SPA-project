from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'duration', 'order', 'user']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons       = LessonSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model  = Course
        fields = [
            'id', 'title', 'description',
            'lessons_count',
            'lessons',
            'user',
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

