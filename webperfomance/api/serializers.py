from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()  # in case you ever swap the default User model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", "")
        )
        # store hashed password (WASM-prehashed or raw) securely
        user.set_password(validated_data["password"])
        user.save()
        return user
