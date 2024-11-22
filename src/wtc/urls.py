from django.urls import path
from .views import *

urlpatterns = [
    path('wtcsubmitdata/', TextDataView.as_view(), name='text-data'),
]