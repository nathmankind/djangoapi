from django.urls import path, include
from django.conf.urls import url
# from django.views.decorators.csrf import csrf_exempt
from .views import AllActionDetail, UserList, UserReg, AuthView, AllActionList, ProjectList, ProjectDetail, ActionList, ActionDetail, ProjectViewset
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'projects', views.ProjectViewset, basename='projects')
router.register(r'projects/<int:id>',
                views.SingleProjectView,
                basename='per_project')
# router.register(r'actions', views.ActionsViewset, basename='actions')
# router.register(r'actions/<int:id>',
#                 views.SingleActionView,
#                 basename='per_action')
# router.register(r'projects_all',
#                 views.ProjectActionViewset,
#                 basename='project_all')
# router.register(r'projects_all/<int:id>',
#                 views.ProjectActionViewset,
#                 basename='project_wt_actions')
# router.register(r'projects_all/<int:id><slug:action>',
#                 views.SingleProjectActionViewset,
#                 basename='project_actions')
# router.register(r'scrumgoals', views.ScrumGoalViewset, basename='scrumgoals')

app_name = "project_api"

urlpatterns = [
    path("users/", UserList.as_view(), name="users_list"),
    path("users/register", UserReg.as_view(), name="users_reg"),
    path("users/auth", AuthView.as_view(), name="users_auth"),
#     path("projects/",
#          ProjectList.as_view(),
#          name="projects2_list"),
#     path("projects/<int:pk>/",
#          ProjectDetail.as_view(),
#          name="projects2_detail"),
    path("projects/<int:pk>/actions/",
         ActionList.as_view(),
         name="action_list"),
    path("projects/<int:project_id>/actions/<int:pk>",
         ActionDetail.as_view(),
         name="action"),
    path("actions/", AllActionList.as_view(), name="all_actions"),
    path("actions/<int:pk>", AllActionDetail.as_view(), name="action_by_id"),
    path('', include(router.urls)),
]
