from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from authentication.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    default_error_messages = {
        'weak_password': _('You need a stronger Password'),
        "small_username": _('You need a longer username')
    }

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, attrs):
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                detail=self.default_error_messages['weak_password'],
                code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if len(attrs['username']) < 4:
            raise serializers.ValidationError(
                detail=self.default_error_messages['small_username'],
                code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        attrs['password'] = make_password(attrs['password'])
        return attrs

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")


class UserTraineeLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserTraineeLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email=attrs.get("email"))
        except User.DoesNotExist:
            raise serializers.ValidationError(
                detail=self.error_messages['invalid_credentials'],
                code=status.HTTP_401_UNAUTHORIZED
            )
        else:
            if not self.user.is_active:
                raise serializers.ValidationError(
                    detail=self.error_messages['inactive_account'],
                    code=status.HTTP_401_UNAUTHORIZED
                )

        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email=attrs.get("email"))
        except User.DoesNotExist:
            raise serializers.ValidationError(
                detail=self.error_messages['invalid_credentials'],
                code=status.HTTP_401_UNAUTHORIZED
            )
        else:
            if not self.user.is_active:
                raise serializers.ValidationError(
                    detail=self.error_messages['inactive_account'],
                    code=status.HTTP_401_UNAUTHORIZED
                )

            self.user = authenticate(email=attrs.get("email"), password=attrs.get('password'))
            if self.user:
                return attrs

            else:
                raise serializers.ValidationError(
                    detail=self.error_messages['invalid_credentials'],
                    code=status.HTTP_401_UNAUTHORIZED
                )

