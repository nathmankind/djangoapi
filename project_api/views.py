from django.shortcuts import render
from .models import User, Project, Action
from .serializers import UserSerializer, ProjectSerializer, ActionSerializer, ProjectActionSerializer
from rest_framework import viewsets
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.response import Response

# Create your views here.


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        username = request.data['username']
        password = request.data['password']
        user, created = User.objects.get_or_create(
            username=request.data['username'])
        if created:
            user.set_password(password)
            # group = Group.objects.get(name=request.data['usertype'])
            # group.user_set.add(user)
            user.save()
            # app_user = User(user=user)
            # app_user.save()
            return JsonResponse({'message': 'User created successfully'})
        else:
            return JsonResponse({'message': 'Error: Username already exist'})


class UserAuthViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @api_view(["POST"])
    @permission_classes((AllowAny))
    def auth(request):
        username = request.data.get('userename')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both user and password'}, status = HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password = password)

        if not user:
            return Response({'error': 'Invalid credentials'},status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user = user)
        return Response({'token': 'token.key'}, status=HTTP_200_OK)


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        name = request.data['name']
        description = request.data['description']
        project = Project(name = name, description = description)
        project.save()
        return JsonResponse({'message': 'Project created successfully'})
        

class SingleProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    
    def project(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id = project_id)
        return Response(project)

    def put(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id = project_id)
        name = request.data['name']
        description = request.data['description']
        completed = request.data['completed']
        project = Project(name = name, description = description, completed = completed)
        project.save()
        return JsonResponse({'message': 'Project details updated successfully'})

    def patch(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id = project_id)
        name = request.data['name']
        description = request.data['description']
        completed = request.data['completed']
        project = Project(name = name, description = description, completed = completed)
        project.save()
        return JsonResponse({'message': 'Project updated successfully'})

    def delete(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id = project_id)
        project.delete()
        return JsonResponse({'message': 'Project deleted successfully'})


class ActionsViewset(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def create(self, request):
        project_id = request.data['project_id']
        project = Project.objects.get(id = int(project_id))
        description = request.data['description']
        note = request.data['note']
        action = Action(project_id = project, description = description, note = note)
        action.save()
        return JsonResponse({'message': 'Action saved successfully'})

class SingleActionView(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    lookup_field = 'id'
    
    def project(self, request, *args, **kwargs):
        action_id = kwargs.get('id', None)
        action = Action.objects.get(id = action_id)
        return Response(project)




class ProjectActionViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectActionSerializer
    lookup_field = 'id'

    def proj_action(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id', None)
        s_project = Project.objects.get(project_id = project_id)
        project_action = s_project.project.all()
        return Response(project_action)
        # description = request.data['description']
        # note = request.data['note']
        # action = Action(project_id = project, description = description, note = note)
        # action.save()
        # return JsonResponse({'message': 'Action saved successfully'})

# class SingleProjectActionViewset(viewsets.ModelViewSet):
#     lookup_field = 'action'
#     def proj_action(self, request, id=None):
#         # queryset = Project.objects.all()
#         project = Project.objects.get(id = project_id)
#         serializer = ProjectActionSerializer(project)
#         # project_action = s_project.action
#         return Response(serializer.action)