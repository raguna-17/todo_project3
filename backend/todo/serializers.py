from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id','username','password','email')

    def create(self, validated):
        user = User(username=validated['username'], email=validated.get('email',''))
        user.set_password(validated['password'])
        user.save()
        return user

class TodoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('id','owner','created_at')

#serializers.py