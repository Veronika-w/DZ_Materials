from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = ("id", "title", "image", "description", "lessons", "owner")


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "image",
            "description",
            "lessons",
            "count_lessons_in_course",
        )
