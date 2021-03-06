from rest_framework import serializers
from articles.models import Article
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from django.contrib.auth.models import User


class ArticlePreviewSerializer(serializers.ModelSerializer):
   class Meta:
       model = Article
       fields = [
           'id',
           'title',
           'created_at',
           'announce',
           'url',
       ]


class ArticleDetailSerializer(serializers.ModelSerializer):
   class Meta:
       model = Article
       fields = [
           'title',
           'created_at',
           'text',
       ]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:

            user_request = get_object_or_404(
                    User,
                    email=email,
                )

            username = user_request.username
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
