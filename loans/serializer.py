from rest_framework import serializers

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ["id", "loan_date", "return_date", "copy", "user"]
        read_only_fields = ["id", "return_date"]
