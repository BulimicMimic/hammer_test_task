from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import AuthorizationCode

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'phone_number',
        )


class TokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    authorization_code = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        authorization_code = attrs['authorization_code']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise NotFound('Такого пользователя не существует.')

        if not AuthorizationCode.objects.filter(
            user=user,
            authorization_code=authorization_code,
        ).exists():
            raise ValidationError(
                {'authorization_code': 'Неверный код авторизации.'}
            )

        jwt_token = RefreshToken.for_user(user)

        authorization = AuthorizationCode.objects.get(
            user=user,
            authorization_code=authorization_code,
        )
        authorization.delete()
        return {
            'access_token': str(jwt_token.access_token),
            'refresh_token': str(jwt_token),
        }
