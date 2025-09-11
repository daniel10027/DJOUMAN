from rest_framework import serializers
from infrastructure.persistence.models import Contract

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ("id","booking","file_url","signed_at","created_at")
        read_only_fields = ("id","created_at")
