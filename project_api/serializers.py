from rest_framework import serializers
from .models import User, Project, Action


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'completed')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'project_id', 'description', 'note')

class ProjectActionSerializer(serializers.ModelSerializer):
    action = ActionSerializer(many = True)
    class Meta:
        model = Project
        fields =  ('id', 'name', 'description', 'completed', 'action')