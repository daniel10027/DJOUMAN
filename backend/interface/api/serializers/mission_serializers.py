from rest_framework import serializers
from infrastructure.persistence.models import Mission

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ("id","booking","freelance","status","started_at","paused_at","stopped_at","completed_at","gps_track","proofs")
        read_only_fields = ("id","freelance","status","started_at","paused_at","stopped_at","completed_at")
