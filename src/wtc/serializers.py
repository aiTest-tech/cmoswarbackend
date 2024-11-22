from rest_framework import serializers
from .models import WTC

class WTCSerializer(serializers.ModelSerializer):
    class Meta:
        model = WTC
        fields = ['id', 'content', 'lang', 'project', 'name', 'occupation', 'address', 'phone',
            'district_corporation', 'taluka_zone', 'village_area', 'subject', 'department',
            'email', 'mode', 'created_at']