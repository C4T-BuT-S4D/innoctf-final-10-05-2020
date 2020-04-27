from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.db.models import Sum, Count, FloatField
from django.db.models.functions import Coalesce, Greatest


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator

    REQUIRED_FIELDS = []

    courses = models.ManyToManyField(
        'Course',
        related_name='users',
        through='UserCourseRelationship',
    )

    SERIALIZED_FIELDS = (
        'id',
        'username',
        'password',
        'first_name',
        'last_name',
    )


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    reward = models.CharField(max_length=255, null=False, blank=False)
    is_finished = models.BooleanField(default=False)

    SERIALIZED_FIELDS = '__all__'

    def get_user_grade(self, user):
        rel = self.uc_rels.filter(user=user).prefetch_related('grades').first()
        if not rel:
            return -1

        grade = rel.grades.aggregate(
            grade=Coalesce(Sum('value'), 1) / Greatest(Coalesce(Count('*', output_field=FloatField()), 0), 0.1),
        )['grade']

        return grade


class Grade(models.Model):
    value = models.FloatField(null=False, blank=False)
    rel = models.ForeignKey('UserCourseRelationship', related_name='grades', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=False, blank=False)

    SERIALIZED_FIELDS = '__all__'


class UserCourseRelationship(models.Model):
    user = models.ForeignKey('User', related_name='uc_rels', on_delete=models.CASCADE, blank=True)
    course = models.ForeignKey('Course', related_name='uc_rels', on_delete=models.CASCADE)

    level = models.CharField(
        max_length=1,
        choices=(
            ('P', 'Pupil'),
            ('T', 'Teacher'),
        ),
        default='P',
    )

    SERIALIZED_FIELDS = '__all__'
