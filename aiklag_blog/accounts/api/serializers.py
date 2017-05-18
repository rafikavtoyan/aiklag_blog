from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    EmailField,
    CharField
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # def validation(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError('This user has already registered')


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        emial2 = value
        if email1 != emial2:
            raise ValidationError("Emails must match")
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError('This user has already registered')

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        emial2 = value
        if email1 != emial2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label='Email Address', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data['password']
        if not email and not username:
            raise ValidationError('Username or Email should be provided')

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('This username|email is not valid')
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect password')
        data['token'] = "some"
        return data

