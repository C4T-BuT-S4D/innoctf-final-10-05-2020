from django.urls import include, re_path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

import api.views

router = SimpleRouter()
router.register('users', api.views.UserViewSet)
router.register('courses', api.views.CourseViewSet)
router.register('relations', api.views.CourseRelationshipViewSet)
router.register('grades', api.views.GradeViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),

    re_path('^me/$', api.views.CurrentUserRetrieveUpdateView.as_view()),
    re_path('^login/$', views.obtain_auth_token),
]
