from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()
    course = LessonSerializer()

    def get_count_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "count_lessons_in_course")
