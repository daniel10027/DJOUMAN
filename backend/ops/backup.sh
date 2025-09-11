#!/usr/bin/env bash
set -e
ts=$(date +%Y%m%d-%H%M%S)
pg_dump "$DATABASE_URL" > "backup-${ts}.sql"
aws s3 cp "backup-${ts}.sql" "s3://$S3_BACKUP_BUCKET/postgres/backup-${ts}.sql"
rm "backup-${ts}.sql"
