from rest_framework import serializers

class DeviceRegisterSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=[("android","Android"),("ios","iOS"),("web","Web")])
    token = serializers.CharField(max_length=255)
