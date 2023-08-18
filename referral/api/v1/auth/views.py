from random import randint
from secrets import token_hex

from sms import send_sms

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.models import AuthorizationCode
from .serializers import TokenSerializer, SignUpSerializer

User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        phone_number = serializer.validated_data['phone_number']
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
        )
        if created:
            invite_code = token_hex(3)
            while User.objects.filter(user_invite_code=invite_code).exists():
                invite_code = token_hex(3)
            user.user_invite_code = invite_code
            user.save()

        authorization_code = randint(0, 9999)
        authorization, _ = AuthorizationCode.objects.get_or_create(
            user=user,
        )
        authorization.authorization_code = authorization_code
        authorization.save()

        send_sms(
            f'Код авторизации: {authorization_code}',
            originator='+79996661234',
            recipients=[phone_number],
            fail_silently=False
        )
        authorization_data = {
            'id': user.id,
            'invite_code': user.user_invite_code,
            'phone_number': phone_number,
            'authorization_code': authorization_code,
        }
        return Response(authorization_data,
                        status=status.HTTP_200_OK,
                        headers=headers,
                        )


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = {
            'access_token': serializer.validated_data['access_token'],
            'refresh_token': serializer.validated_data['refresh_token'],
        }
        return JsonResponse(data=response_data)
