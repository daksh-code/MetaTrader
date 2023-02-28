from dataclasses import field
from pyexpat import model
from rest_framework import serializers

from authTokens.models import AuthToken

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=AuthToken
        fields = ('api_access_token', 'api_refresh_token','api_consumer_key','api_account_number','multiplier')
