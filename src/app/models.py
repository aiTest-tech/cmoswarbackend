from django.db import models
from base.models import BaseModel, Data
from auth_app.models import User, Project
# Create your models here.


# class AudioRecord(BaseModel):
#     audio_file = models.FileField(upload_to='audio_files/', null=True, blank=True)
#     source = models.TextField()
#     edit_source = models.TextField(null=True, blank=True)
#     sentiment_analysis = models.IntegerField(null =True, blank=True)
    
#     def __str__(self):
#         return f"Audio-recorder-{self.id}"
    
class ASRData(BaseModel):
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="asr_data")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    min = models.IntegerField()
    is_succ = models.BooleanField(default=False)
    api_hit = models.IntegerField(default=0)

    def __str__(self):
        return f"ASR Data {self.id} - Success: {self.is_succ}"


# class RatingRecord(models.Model):
#     audio_id = models.ForeignKey(AudioRecord, on_delete=models.CASCADE)
#     rating = models.CharField(max_length=100)
    
#     def __str__(self):
#         return f"rating-{self.rating}, {self.audio_id}"