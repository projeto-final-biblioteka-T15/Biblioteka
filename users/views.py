from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwner
from loans.models import Loan
from loans.serializer import LoanSerializer
from rest_framework.response import Response 


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        password = self.request.data.get("password", None)
        instance = serializer.save()

        if password is not None:
            instance.set_password(password)
            instance.save()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        loans = Loan.objects.filter(user=instance)
        loan_serializer = LoanSerializer(loans, many=True)
        data = serializer.data
        data['loans'] = loan_serializer.data
        return Response(data)

