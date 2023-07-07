from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from loans.serializer import LoanSerializer
from .models import Loan
from books.permissions import IsLibraryStaff
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


class LoanView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        user = self.request.user

        if user.user_type != 'library_staff':
            raise PermissionDenied("Você não tem permissão para criar empréstimos.")

        loan = serializer.save()
        loan.copy.loan_copy()
    
    def perform_update(self, serializer):
        loan = serializer.save()
        if loan.returned:
            loan.copy.return_copy()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.user_type == 'student':
            queryset = queryset.filter(user=user)
        
        user_id = self.request.query_params.get('user_id')
        pending_returns = self.request.query_params.get('pending')

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if pending_returns:
            queryset = queryset.filter(returned=False)

        return queryset

    

class LoanReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.returned:
            return Response({"detail": "O livro já foi devolvido."}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.returned = True
        instance.return_made = timezone.now().date()

        instance.save()

        instance.copy.return_copy()

        instance.check_return_date()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
