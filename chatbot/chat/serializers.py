from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChatGroup, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'group', 'sender', 'sender_username', 'content', 'timestamp']

class ChatGroupSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'members', 'messages']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=ChatGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'groups']

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.chat_groups.set(groups)
        return user
