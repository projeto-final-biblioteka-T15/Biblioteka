from rest_framework import serializers
from .models import Loan
from users.models import User
from copies.models import Copies
from datetime import timedelta, date


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    copy = serializers.PrimaryKeyRelatedField(queryset=Copies.objects.all())

    loan_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    return_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    returned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "loan_date", "return_date", "returned"]

    def create(self, validated_data):
        user = validated_data["user"]
        copy = validated_data["copy"]

        if user.is_blocked:
            raise serializers.ValidationError("Usuário bloqueado.")

        if copy.available == 0:
            raise serializers.ValidationError("Não há cópias disponíveis para empréstimo.")

        copy.available -= 1
        copy.save()

        loan_date = date.today()
        return_date = loan_date + timedelta(days=7) 
        while return_date.weekday() >= 5:  
            return_date += timedelta(days=1) 
        

        loan = Loan.objects.create(copy=copy, user=user, loan_date=loan_date, return_date=return_date)
        return loan

