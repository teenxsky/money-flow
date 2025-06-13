from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import CharField, EmailField, IntegerField, Serializer
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class UserRegisterSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True, validators=[validate_password])
    first_name = CharField(required=True, max_length=50)
    last_name = CharField(required=True, max_length=50)

    def validate_email(self, value):
        norm_email = value.lower()

        unique_validator = UniqueValidator(queryset=User.objects.all())
        unique_validator(norm_email, self.fields['email'])

        return norm_email


class UserLoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)

    def validate_email(self, value):
        return value.lower()


class UserDetailSerializer(Serializer):
    id = IntegerField()
    email = EmailField()
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)


class UserLogoutSerializer(Serializer):
    refresh = CharField(required=True)
