from rest_framework import serializers

class EmptySerializer(serializers.Serializer):
    """Serializer vide, juste pour que drf-spectacular ait un nom stable."""
    class Meta:
        ref_name = "Empty"  # évite les collisions & noms vides
