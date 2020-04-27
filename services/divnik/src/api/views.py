from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, mixins

import api.models
import api.serializers


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        login(request, user)

        serializer = api.serializers.UserSerializer(instance=user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        logout(request)
        return Response('ok')


class UserViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = api.models.User.objects.all()
    serializer_class = api.serializers.UserSerializer
    permission_classes = (AllowAny,)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = api.models.Course.objects.all()
    serializer_class = api.serializers.CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'get_reward':
            return api.serializers.CourseRewardSerializer
        return super(CourseViewSet, self).get_serializer_class()

    def check_object_permissions(self, request, obj: api.models.Course):
        super(CourseViewSet, self).check_object_permissions(request, obj)

        if self.action == 'retrieve':
            return

        if self.action == 'get_reward':
            if not obj.is_finished:
                raise PermissionDenied('Course is not finished')

            grade = obj.get_user_grade(self.request.user)

            if grade < 5:
                raise PermissionDenied('Haven\'t earned the reward')

            return

        if not obj.uc_rels.filter(level='T', user=request.user).exists():
            self.permission_denied(request, 'No access')

    @action(methods=['get'], detail=True, url_path='reward')
    def get_reward(self, request, *args, **kwargs):
        return super(CourseViewSet, self).retrieve(request, *args, **kwargs)


class CourseRelationshipViewSet(viewsets.ModelViewSet):
    queryset = api.models.UserCourseRelationship.objects.all()
    serializer_class = api.serializers.CourseRelationshipSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = ('course', 'user')

    def check_object_permissions(self, request, obj):
        super(CourseRelationshipViewSet, self).check_object_permissions(request, obj)
        if not obj.user != request.user:
            self.permission_denied(request, 'No access')


class GradeViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = api.models.Grade.objects.all()
    serializer_class = api.serializers.GradeSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = ('rel',)

    def get_serializer_class(self):
        if self.action == 'get_comment':
            return api.serializers.GradeCommentSerializer
        return super(GradeViewSet, self).get_serializer_class()

    def check_object_permissions(self, request, obj):
        super(GradeViewSet, self).check_object_permissions(request, obj)

        if self.action == 'get_comment':
            if obj.rel.user == self.request.user:
                return

            rels = api.models.UserCourseRelationship.objects.filter(user=self.request.user, level='T')
            if rels.exist():
                return

            self.permission_denied(request, 'No access')

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, *args, **kwargs):
        return super(GradeViewSet, self).retrieve(request, *args, **kwargs)
