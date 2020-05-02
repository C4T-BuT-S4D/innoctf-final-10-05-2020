from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

import api.models
import api.pagination
import api.serializers


class CurrentUserRetrieveUpdateView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = api.models.User.objects.all()
    serializer_class = api.serializers.UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = api.models.User.objects.all()
    serializer_class = api.serializers.UserSerializer
    pagination_class = api.pagination.UserPagination
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

        rel = obj.uc_rels.filter(user=request.user).first()

        if not rel:
            raise PermissionDenied('Not a participant')

        if rel.level == 'T':
            return

        if self.action != 'get_reward':
            raise PermissionDenied('No access')

        if not obj.is_finished:
            raise PermissionDenied('Course is not finished')

        grade = obj.get_user_grade(self.request.user)

        if grade < 5:
            raise PermissionDenied('Haven\'t earned the reward')

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
            if rels.exists():
                return

            self.permission_denied(request, 'No access')

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, *args, **kwargs):
        return super(GradeViewSet, self).retrieve(request, *args, **kwargs)
