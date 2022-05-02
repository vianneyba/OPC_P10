from rest_framework.serializers import ModelSerializer
from authenticate.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'first_name',
            'last_name', 'email', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}}

    def create(self, data):
        user = User.objects.create_user(
            data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        return user


class UserProjectSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']
