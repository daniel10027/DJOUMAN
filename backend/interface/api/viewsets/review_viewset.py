from rest_framework import viewsets, mixins, permissions
from interface.api.serializers.review_serializers import ReviewSerializer
from infrastructure.persistence.models import Review

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Review"])
class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.select_related("author","target_user","booking").all().order_by("-id")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
