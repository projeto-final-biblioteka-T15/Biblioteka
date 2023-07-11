from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner
from rest_framework.views import Response, status


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   


class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = self.request.query_params.get("user_id")

        if self.request.user.user_type == "library_staff" and user_id:
            user = get_object_or_404(queryset, id=user_id)
            queryset = User.objects.filter(id=user.id)
        elif self.request.user.user_type == "student":
            queryset = User.objects.filter(id=self.request.user.id)

        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_update(self, serializer):
        password = self.request.data.get("password", None)
        instance = serializer.save()

        if password is not None:
            instance.set_password(password)
            instance.save()
