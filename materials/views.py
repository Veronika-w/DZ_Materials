from rest_framework.decorators import permission_classes
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.permissions import IsOwnerOrStaff

from .models import Course, Lesson
from .serializers import (CourseDetailSerializer, CourseSerializer,
                          LessonSerializer)
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == "create":
            classes = [IsAuthenticated & ~IsModer]
        elif self.action in ("retrieve", "update", "partial_update"):
            classes = [IsAuthenticated & (IsModer | IsOwner)]
        elif self.action == "destroy":
            classes = [IsAuthenticated & ~IsModer & IsOwner]
        else:
            classes = [IsAuthenticated]

        return [permission() for permission in classes]


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def get_queryset(self):
        if self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
