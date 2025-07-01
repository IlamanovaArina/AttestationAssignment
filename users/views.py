import logging
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


logger = logging.getLogger('users')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id').distinct()
    permission_classes = [AllowAny]
