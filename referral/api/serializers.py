from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

User = get_user_model()


class UserPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number',)


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(read_only=True)
    user_invite_code = serializers.CharField(read_only=True)
    activated_code = serializers.CharField()
    invited_users = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'phone_number',
            'user_invite_code',
            'activated_code',
            'invited_users',
        )
        read_only_fields = (
            'id',
            'phone_number',
            'user_invite_code',
            'invited_users',
        )

    def get_invited_users(self, obj):
        request = self.context['request']
        invited_list = User.objects.filter(activated_code=obj.user_invite_code)
        return UserPhoneSerializer(
            invited_list,
            many=True,
            context={'request': request},
            ).data

    def validate_activated_code(self, value):
        user = self.context['request'].user
        if user.activated_code:
            raise serializers.ValidationError('Инвайт код уже применен.')
        if value == user.user_invite_code:
            raise serializers.ValidationError(
                'Нельзя применить собственный инвайт код.')
        if not User.objects.filter(user_invite_code=value).exists():
            raise serializers.ValidationError(
                'Такого кода не существует.')
        return value
