from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import api.models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.User
        fields = api.models.User.SERIALIZED_FIELDS

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        user = api.models.User.objects.create_user(**validated_data, is_active=True)
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Course
        fields = api.models.Course.SERIALIZED_FIELDS

        extra_kwargs = {
            'reward': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        instance = super(CourseSerializer, self).create(validated_data)
        cur_user = self.context['request'].user
        rel = api.models.UserCourseRelationship(user=cur_user, course=instance, level='T')
        rel.save()
        return instance


class CourseRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Course
        fields = ('reward',)


class CourseRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.UserCourseRelationship
        fields = api.models.UserCourseRelationship.SERIALIZED_FIELDS

    def update(self, instance, validated_data):
        validated_data['level'] = instance.level
        super(CourseRelationshipSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        super(CourseRelationshipSerializer, self).create(validated_data)


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Grade
        fields = api.models.Grade.SERIALIZED_FIELDS

        extra_kwargs = {
            'comment': {
                'write_only': True,
            },
        }

    def validate(self, attrs):
        rel = attrs.get('rel')
        if isinstance(rel, int):
            rel = api.models.UserCourseRelationship.objects.filter(id=rel).first()

        if not rel:
            raise ValidationError({'rel': 'invalid relation'})

        cur_user = self.context['request'].user
        if not rel.course.uc_rels.filter(level='T', user=cur_user).exists():
            raise ValidationError({'rel': 'can\'t grade this student'})

        return attrs


class GradeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.models.Grade
        fields = ('comment',)
