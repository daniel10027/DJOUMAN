from rest_framework import serializers
from infrastructure.persistence.models import KycDocument, KycStatus

class KycSerializer(serializers.ModelSerializer):
    class Meta:
        model = KycDocument
        fields = ("id","user","doc_type","file_url","data","status","reviewed_by","reviewed_at","created_at")
        read_only_fields = ("id","status","reviewed_by","reviewed_at","created_at","user")
