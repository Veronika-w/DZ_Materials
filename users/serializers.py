from rest_framework import serializers

from .models import User, Payments


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    payments = PaymentsSerializer(many=True,
                                  read_only=True,
                                  source="payments_set")

    class Meta:
        model = User
        fields = ("id",
            "email",
            "password",
            "phone",
            "city",
            "avatar",
            "payments")

        read_only_fields = ("id", "payments")

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
