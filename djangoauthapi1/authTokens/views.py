from asyncio import streams
import io
from typing import IO
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from account.models import User

from .models import AuthToken
from .serializers import AuthTokenSerializer
# Create your views here.


class AuthTokenView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        token_profile = AuthToken.objects.get(user=request.user.id)
        print(token_profile,"AAAAEWWESDSDSAFFSASASASASASASASA")
        serializer = AuthTokenSerializer(token_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        token_profile = AuthToken.objects.get(user=request.user.id)
        serializer=AuthTokenSerializer(token_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
