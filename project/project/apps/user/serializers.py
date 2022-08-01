from django.dispatch import receiver
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserBluePrintSerializers(serializers.ModelSerializer):

    class Meta:
        abstract = True
        model = User
        fields = ('id', 'full_name', 'pic')



class SnippetAuthorSerializer(UserBluePrintSerializers):
    pass


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday', 'avatar', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, attrs):
        data = super(UserCreationSerializer, self).to_representation(attrs)
        refresh = TokenObtainPairSerializer.get_token(self.instance)
        data['avatar'] = self.instance.pic()
        data['auth'] = {}
        data['auth']['refresh'] = str(refresh)
        data['auth']['access'] = str(refresh.access_token)
        return data

    

class UserProfileSerializer(UserBluePrintSerializers):
    following = serializers.SerializerMethodField(
        method_name='is_visitor_following_user')
    follower = serializers.SerializerMethodField(method_name='is_user_following_visitor')

    def is_visitor_following_user(self, user):
        visitor = self.context.get('visitor')
        return user in visitor.following.all()

    def is_user_following_visitor(self, user):
        visitor = self.context.get('visitor')
        return visitor in user.following.all()


    class Meta(UserBluePrintSerializers.Meta):
        fields = UserBluePrintSerializers.Meta.fields + \
            ('bio', 'following', 'follower')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user': SnippetAuthorSerializer(self.user).data})
        return data