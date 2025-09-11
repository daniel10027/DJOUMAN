import boto3
from django.conf import settings

class S3Adapter:
    def __init__(self):
        self.bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        key = getattr(settings, "AWS_ACCESS_KEY_ID", None)
        secret = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
        endpoint = getattr(settings, "AWS_S3_ENDPOINT_URL", None)

        if not all([self.bucket, key, secret, endpoint]):
            raise RuntimeError("S3 non configuré : définissez AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "
                               "AWS_STORAGE_BUCKET_NAME et AWS_S3_ENDPOINT_URL")

        self.client = boto3.client(
            "s3",
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            endpoint_url=endpoint,
        )

    def presign_upload(self, *, path: str, content_type: str, expires: int = 3600) -> dict:
        return self.client.generate_presigned_post(
            Bucket=self.bucket,
            Key=path,
            Fields={"Content-Type": content_type},
            Conditions=[{"Content-Type": content_type}],
            ExpiresIn=expires,
        )
