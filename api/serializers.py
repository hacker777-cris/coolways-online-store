from rest_framework import serializers
from store.models import Product, UserProfile
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "quantity", "image", "description"]


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "phone_number",
            "email",
            "profile_picture",
        ]

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        return data

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        validated_data.pop(
            "confirm_password"
        )  # Remove confirm_password as it is not needed for User

        # Create the user
        new_user = User.objects.create_user(
            username=username, password=password, email=validated_data.pop("email")
        )

        # Update the user profile with the additional data
        new_user.userprofile.phone_number = validated_data.get("phone_number")
        new_user.userprofile.profile_picture = validated_data.get("profile_picture")
        new_user.userprofile.save()

        return new_user
