from django.urls import path
from .views import *

urlpatterns = [
    path("speech-to-text/", ProcessAudioView.as_view(), name="process_audio"),
    path("submit-audio/", SubmitAudioView.as_view(), name=""),
    path("show/", FetchAllAudioRecordsView.as_view(), name="show"),
]