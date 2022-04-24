from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authenticate.serializers import UserSerializer


class SignUpView(APIView):

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
