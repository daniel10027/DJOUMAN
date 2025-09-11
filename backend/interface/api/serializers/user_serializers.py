from rest_framework import serializers
from infrastructure.persistence.models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("name", "avatar", "bio", "address", "geo_lat", "geo_lng")

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone", "role", "status", "profile")
        read_only_fields = ("id", "role", "status")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if profile_data is not None:
            prof = getattr(instance, "profile", None)
            if not prof:
                prof = Profile.objects.create(user=instance)
            for k, v in profile_data.items():
                setattr(prof, k, v)
            prof.save()
        return instance
