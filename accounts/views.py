from rest_framework import generics
from serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
