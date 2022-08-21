from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from account.utils.serializers import BaseUserSerializer


# Create your views here.


class Register(APIView):
    def post(self, request):
        serializer = BaseUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

