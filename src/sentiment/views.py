from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from .serializers import AnalyzeSerializer
from .models import SentimentData
import json
from rest_framework.permissions import IsAuthenticated


model_name = "/home/cmoai/Models"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class AnalyzeSentiment(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AnalyzeSerializer)  
    def post(self, request, *args, **kwargs):
        try:
            serializer = AnalyzeSerializer(data=request.data)
            
            if serializer.is_valid():
                lang = serializer.validated_data.get("lang", None)
                text_data = serializer.validated_data.get("data", None)

                if lang == 'gu':
                    text_data = GoogleTranslator(source='gu', target='en').translate(text_data)
                    print(text_data)
                
                elif lang == 'gu' and text_data is None:
                    text_data = ""
                

                encoded_input = tokenizer(text_data, return_tensors='pt')
                output = model(**encoded_input)
                scores = output[0][0].detach().numpy()
                scores = softmax(scores)  
                labels = ["Negative", "Neutral", "Positive"]
                sentiment = {label: score for label, score in zip(labels, scores)}
                max_label = max(sentiment, key=sentiment.get)
                max_score = sentiment[max_label]

                sentiment_record = SentimentData.objects.create(
                    lang=lang,
                    text_data=text_data,
                    label=max_label,
                    score=max_score
                )
                sentiment_record.save()

                result = {
                        "sentiment": max_label,
                        "gravity": max_score
                    }

                return Response(result, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
