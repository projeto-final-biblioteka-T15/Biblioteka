from rest_framework import serializers
from .models import Loan
from users.models import User
from copies.models import Copies
from datetime import timedelta, date


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    copy = serializers.PrimaryKeyRelatedField(queryset=Copies.objects.all())

    loan_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    #return_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    return_date = serializers.DateField(format="%Y-%m-%d") #para teste usuário bloqueado
    returned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "loan_date", "return_date", "returned", "return_made"]

    def create(self, validated_data):
        user = validated_data["user"]
        copy = validated_data["copy"]

        if user.is_blocked:
            raise serializers.ValidationError("Usuário bloqueado.")

        if copy.available == 0:
            raise serializers.ValidationError("Não há cópias disponíveis para empréstimo.")
        
        active_loan = Loan.objects.filter(user=user, copy=copy, returned=False).first()
        if active_loan:
            raise serializers.ValidationError("O usuário já possui um empréstimo ativo para esta cópia.")

        loan_date = date.today()
        return_date = validated_data.get("return_date") #para teste usuário bloqueado
        # return_date = loan_date + timedelta(days=7) 
        # while return_date.weekday() >= 5:  
        #     return_date += timedelta(days=1) 
        

        loan = Loan.objects.create(copy=copy, user=user, loan_date=loan_date, return_date=return_date)
        return loan
