from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from loans.serializer import LoanSerializer
from .models import Loan
from books.permissions import IsLibraryStaff
from rest_framework.response import Response


class LoanView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        loan = serializer.save()
        loan.copy.loan_copy()

    def perform_update(self, serializer):
        loan = serializer.save()
        if loan.returned:
            loan.copy.return_copy()

class LoanReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.returned = True
        instance.save()

        instance.copy.return_copy()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
