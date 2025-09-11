from rest_framework import serializers

class PushNotificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    title = serializers.CharField(max_length=120)
    body = serializers.CharField(max_length=500)
    data = serializers.DictField(
        child=serializers.CharField(allow_blank=True),
        required=False
    )

class EmailNotificationSerializer(serializers.Serializer):
    to = serializers.EmailField()
    subject = serializers.CharField(max_length=160)
    html = serializers.CharField()

class SmsNotificationSerializer(serializers.Serializer):
    to = serializers.CharField(max_length=32)
    message = serializers.CharField(max_length=160)

# (Optionnel) Réponses uniformes pour la doc
class NotificationResponseSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["sent"])
