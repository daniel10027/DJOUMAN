from rest_framework import viewsets, permissions, decorators, response, status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from infrastructure.providers.storage.s3_adapter import S3Adapter

@extend_schema(tags=["Storage"])
class StorageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Storage"], summary="Générer une URL de mise en ligne (presign)",
        request=None,
        responses={200: OpenApiResponse(description="Presign OK")},
        examples=[OpenApiExample("PresignReq", value={"path": "uploads/avatars/u1.png", "content_type": "image/png"}, request_only=True)],
    )
    @decorators.action(detail=False, methods=["post"], url_path="presign")
    def presign(self, request):
        path = request.data.get("path")
        content_type = request.data.get("content_type", "application/octet-stream")
        if not path:
            return response.Response({"error": "path required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            adapter = S3Adapter()
            data = adapter.presign_upload(path=path, content_type=content_type)
            return response.Response(data)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
