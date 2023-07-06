from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Copies
from loans.models import Loan
from .serializers import CopiesSerializer
from .permissions import IsLibraryStaffOrAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from books.permissions import IsLibraryStaff


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaffOrAuthenticated | IsAuthenticatedOrReadOnly]

    queryset = Copies.objects.all()
    serializer_class = CopiesSerializer


class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryStaff]

    queryset = Copies.objects.all()
    serializer_class = CopiesSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        allowed_fields = set(["total", "available"])
        updated_fields = set(request.data.keys())
        if not updated_fields.issubset(allowed_fields):
            raise ValidationError("Apenas os campos 'total' e 'available' podem ser alterados.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        loan = Loan.objects.filter(copy=instance, returned=False).first()
        if loan:
            instance.check_user_blocked(loan.user)

        return Response(serializer.data)
