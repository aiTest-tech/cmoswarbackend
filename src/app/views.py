import base64
import json
import os
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AudioRecord
from .serializers import *


ASR_API_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
ASR_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("BHASHINI_AUTHORIZATION")
}

class ProcessAudioView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AudioRecordSerializer)
    def post(self, request):

        print("request.data:", request.data)
        serializer = AudioRecordSerializer(data=request.data)

        # Validate incoming data using the serializer
        if not serializer.is_valid():
            missing_fields = []

            if 'file' not in request.FILES:
                missing_fields.append('file')
            if 'lang' not in request.data:
                missing_fields.append('lang')

            return Response(
                {"errors": serializer.errors, "missing_fields": missing_fields},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = serializer.validated_data['file']
        lang = serializer.validated_data['lang']

        base64_audio = base64.b64encode(file.read()).decode('utf-8')

        service_id = (
            "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4"
            if lang != "en"
            else "ai4bharat/whisper-medium-en--gpu--t4"
        )

        payload = {
            "pipelineTasks": [{
                "taskType": "asr",  
                "config": {
                    "preProcessors": ["vad"],  
                    "language": {"sourceLanguage": lang},  
                    "serviceId": service_id,  
                    "audioFormat": "wav",  
                    "samplingRate": 16000,  
                },
            }],
            "inputData": {
                "audio": [{"audioContent": base64_audio}],  
            },
        }

        response = requests.post(ASR_API_URL, headers=ASR_API_HEADERS, data=json.dumps(payload))

        if response.status_code != 200:
            return Response(
                {"error": "Failed to process audio"},
                status=response.status_code,
            )

        response_data = response.json()
        source_text = response_data['pipelineResponse'][0]['output'][0]['source']

        record = AudioRecord.objects.create(source=source_text, audio_file=file)

        return Response(
            {"text": source_text, "id": record.id},
            status=status.HTTP_200_OK,
        )

class SubmitAudioView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SubmitAudioSerializer)
    def post(self, request):

        serializer = SubmitAudioSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record_id = serializer.validated_data['id']
        text = serializer.validated_data['text']

        try:
            record = AudioRecord.objects.get(id=record_id)

            record.edit_source = text
            record.sentiment_analysis = 0
            record.save()  

            return Response(
                {"status": "success", "message": "Record updated successfully"},
                status=status.HTTP_200_OK,
            )

        except AudioRecord.DoesNotExist:
            return Response(
                {"status": "fail", "message": "Record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        
class FetchAllAudioRecordsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        records = AudioRecord.objects.values(
            'id', 'audio_file', 'source', 'edit_source', 'created_at', 'updated_at'
        )

        total_count = AudioRecord.objects.all().count()

        response_data = {
            "total_number": total_count,  
            "data": list(records),       
        }

        return JsonResponse(
            response_data, safe=False, status=status.HTTP_200_OK
        )


