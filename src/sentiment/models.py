from django.db import models

class SentimentAnalysis(models.Model):
    lang = models.CharField(max_length=10)
    text_data = models.TextField()
    label = models.CharField(max_length=20)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)