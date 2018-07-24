from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the clientself.

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The clieant should not be able to send a token along with a registration
    # request. making `token` read-only and handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.

        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255,read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):
        # `validate` method is an instance of `LoginSerializer`
        # that checks for valid credentials. Validating for
        # email and password to make sure it matches user in
        # database
        email = data.get('email',None)
        password = data.get('password', None)

        # Raise an exception if email is not provided
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an except if password is not provided

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # `authenticate` method is provided by Django to handle checking
        # of user that matches email/password combination.
        # email is the username because in models,
        # `USERNAME_FIELD` was set as `email`

        user = authenticate(username=email, password=password)

        # Raise exception if user does not match the email and/or password provided

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        # The `validate` method will return a dictonary of validated data.
        # This is the data that will be passed into the `create` and `update` methods

        return{
            'email': email,
            'username': user.username,
            'token': user.token
        }
