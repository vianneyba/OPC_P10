from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authenticate.serializers import UserSerializer
from django.db import IntegrityError
from django.contrib.auth.password_validation import (
    CommonPasswordValidator, MinimumLengthValidator,
    NumericPasswordValidator, validate_password)
from django.core.exceptions import ValidationError


class SignUpView(APIView):

    serializer_class = UserSerializer

    def post(self, request):
        try:
            validate_password(self.request.data['password'],
                              [MinimumLengthValidator,
                              CommonPasswordValidator,
                              NumericPasswordValidator])
        except ValidationError as errors:
            return Response(
                {"detail": errors},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'errors': 'user exists'},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
