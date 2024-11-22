from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
# from .models import TextData


from django.views import View

# Create your views here.
def analytics(request):
    if request.method == "GET":
        data = {
            "asr": [
                {"project": "WTC", "total_minutes_called": 1200, "total_requests": 150, "success_rate": 80.0},
                {"project": "GS", "total_minutes_called": 500, "total_requests": 100, "success_rate": 20.0}
            ],
            "sentiment": [
                {"project": "WTC", "total_requests": 300, "success_rate": 85.33},
                {"project": "GS",  "total_requests": 70, "success_rate": 25.0}
            ],
            "l1_scrutiny": [
                {"project": "WTC", "total_requests": 500, "success_rate": 92.0},
                {"project": "GS", "total_requests": 89, "success_rate": 46.0}
            ],
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request method"}, status=405)