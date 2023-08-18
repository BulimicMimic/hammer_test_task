from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from api.permissions import IsCurrentUserOrAdminOrReadOnly
from api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCurrentUserOrAdminOrReadOnly,)
