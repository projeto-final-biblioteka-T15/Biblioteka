from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "name", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user_type = validated_data.get("user_type")

        if user_type == "library_staff":
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        password = validated_data.pop("password")
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context["request"].method == "POST":
            representation.pop("email")
        return representation
