from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import TextData
from .serializers import TextDataSerializer
import os
import random
import string
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

def hello_world(request):
    return JsonResponse({"message": "Hello, API!"})

class TextDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        texts = TextData.objects.all()
        serializer = TextDataSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TextDataSerializer)
    def post(self, request):
        serializer = TextDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)