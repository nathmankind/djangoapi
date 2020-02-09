from django.urls import path, include
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users/register', views.UserViewset, basename='users')
router.register(r'users/auth', views.UserAuthViewset, basename='auth')
router.register(r'projects', views.ProjectViewset, basename='projects')
router.register(r'projects/<int:id>',
                views.SingleProjectView,
                basename='per_project')
router.register(r'actions', views.ActionsViewset, basename='actions')
router.register(r'actions/<int:id>',
                views.SingleActionView,
                basename='per_action')
router.register(r'projects_all',
                views.ProjectActionViewset,
                basename='project_all')
router.register(r'projects_all/<int:id>',
                views.ProjectActionViewset,
                basename='project_actions')
# router.register(r'projects_all/<int:id><slug:action>',
#                 views.SingleProjectActionViewset,
#                 basename='project_actions')
# router.register(r'scrumgoals', views.ScrumGoalViewset, basename='scrumgoals')

app_name = "project_api"

urlpatterns = [
    path('', include(router.urls)),
]