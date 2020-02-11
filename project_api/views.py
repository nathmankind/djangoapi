from django.shortcuts import render, get_object_or_404
from .models import Project, Action
from django.contrib.auth.models import User
from .serializers import UserSerializer,RegUserSerializer, ProjectSerializer, ActionSerializer, ProjectActionSerializer
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.response import Response


# Create your views here.

#List all users
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data)

#User registration
class UserReg(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegUserSerializer

#Authentication
class AuthView(APIView):
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


#Get all projects
class ProjectList( APIView):
    def post(self, request):
        name = request.data['name']
        description = request.data['description']
        project = Project(name=name, description=description)
        project.save()
        return JsonResponse({'message': 'Project created successfully'})

    

#Retrieve all and create projects
class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        name = request.data['name']
        description = request.data['description']
        project = Project(name=name, description=description)
        project.save()
        return JsonResponse({'message': 'Project created successfully'})


#get project by id, put, patch, delete
class SingleProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def project(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id=project_id)
        return Response(project)

    def put(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id=project_id)
        name = request.data['name']
        description = request.data['description']
        completed = request.data['completed']
        project = Project(name=name,
                          description=description,
                          completed=completed)
        project.save()
        return JsonResponse(
            {'message': 'Project details updated successfully'})

    def patch(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id=project_id)
        name = request.data['name']
        description = request.data['description']
        completed = request.data['completed']
        project = Project(name=name,
                          description=description,
                          completed=completed)
        project.save()
        return JsonResponse({'message': 'Project updated successfully'})

    def delete(self, request, *args, **kwargs):
        project_id = kwargs.get('id', None)
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({'message': 'Project deleted successfully'})


#Create a new action under an existing project
class ActionList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Action.objects.filter(project_id=self.kwargs["pk"])
        return queryset
    serializer_class = ActionSerializer


#Retrieve all actions
class AllActionList(APIView):
    def get(self, request):
        actions = Action.objects.all()
        data = ActionSerializer(actions, many=True).data
        return Response(data)


#Retrieve all actions for a particular project   
class ActionList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Action.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = ActionSerializer
 
 #Retrieve a single action by ID
class SingleActionView(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    lookup_field = 'id'

    def project(self, request, *args, **kwargs):
        action_id = kwargs.get('id', None)
        action = Action.objects.get(id=action_id)
        return Response(project)

#Retrieve a single action by ID
class AllActionDetail(APIView):
    def get(self, request, pk):
        action = get_object_or_404(Action, pk=pk)
        data = ActionSerializer(action).data
        return Response(data)

#Retrieve a single action by ID 4 params
class ActionDetail(APIView):
    def get(self, request, pk, project_id):
        action = get_object_or_404(Action, project_id = project_id, id=pk)
        data = ActionSerializer(action).data
        return Response(data)
    
    #Update an action
    def put(self, request, pk, project_id):
        action = get_object_or_404(Action, project_id = project_id, id=pk)
        serializer = ActionSerializer(action, data = request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(
            {'message': 'Action details updated successfully'})

    #Delete an action    
    def delete(self, request, pk, project_id):
        action = get_object_or_404(Action, project_id = project_id, id=pk)
        action.delete()
        return Response({"message": "Action has been deleted."},status=204)


class ActionsViewset(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def create(self, request):
        project_id = request.data['project_id']
        project = Project.objects.get(id=int(project_id))
        description = request.data['description']
        note = request.data['note']
        action = Action(project_id=project, description=description, note=note)
        action.save()
        return JsonResponse({'message': 'Action saved successfully'})


class SingleActionView(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    lookup_field = 'id'

    def project(self, request, *args, **kwargs):
        action_id = kwargs.get('id', None)
        action = Action.objects.get(id=action_id)
        return Response(project)


class ProjectActionViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectActionSerializer
    lookup_field = 'id'

    def proj_action(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id', None)
        s_project = Project.objects.get(project_id=project_id)
        project_action = s_project.project.all()
        return Response(project_action)


class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        data = ProjectActionSerializer(projects, many=True).data
        return Response(data)


class ProjectDetail(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        data = ProjectActionSerializer(project).data
        return Response(data)