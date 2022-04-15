from rest_framework import generics

from gametime_auth.api.serializers import UserSerializer
from gametime_auth.models import User


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
