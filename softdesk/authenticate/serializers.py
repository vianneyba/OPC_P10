from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name',
            'last_name', 'email', 'password'
        ]

    def create(self, data):
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        return user
