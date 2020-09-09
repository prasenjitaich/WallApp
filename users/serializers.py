from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    serializer to handle turning our `User` object into
    something that can be JSONified and sent to the client
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Function is used to create user object with serializer.
        :param validated_data: keep all user related data.
        :return: user object.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Function is used for the update user information.
        :param instance: user object instance
        :param validated_data: new info passed in request.
        :return: user object.
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'created_on',
                  'modified_on')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    custom serializer for get user_id, username, first_name fields with token response.
    """

    def validate(self, attrs):
        """
        function is used for validate token and add extra fields.
        :param attrs: get username and password
        :return: dictionary with tokens, user_id and username
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data
