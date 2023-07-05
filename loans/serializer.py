from rest_framework import serializers
from .models import Loan
from users.models import User
from copies.models import Copies

from datetime import timedelta
from django.utils import timezone


# class LoanSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Loan
#         fields = ["id", "loan_date", "return_date", "copy", "user"]
#         read_only_fields = ["id", "return_date"]


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    copy = serializers.PrimaryKeyRelatedField(queryset=Copies.objects.all())

    loan_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    return_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "loan_date", "return_date", "returned"]
        read_only_fields = ["id", "return_date", "loan_date", "returned"]

    def create(self, validated_data):
        user = validated_data["user"]
        copy = validated_data["copy"]

        if copy.available == 0:
            raise serializers.ValidationError(
                "Não há cópias disponíveis para empréstimo."
            )

        copy.available -= 1
        copy.save()

        existing_loans = Loan.objects.filter(copy=copy)
        if existing_loans:
            raise serializers.ValidationError("Este livro já está emprestado.")

        loan_date = timezone.localdate()
        return_date = loan_date + timedelta(days=7)
        while return_date.weekday() >= 5:
            return_date += timedelta(days=1)

        loan = Loan.objects.create(
            copy=copy, user=user, loan_date=loan_date, return_date=return_date
        )
        return loan
