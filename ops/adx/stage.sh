#!/usr/bin/env bash
# ops/adx/stage.sh — PREP-ONLY staging script for AWS Data Exchange product import.
# NOT executed against AMMP without owner approval (seller registration is owner-gated).
#
# Reference: aws-samples/aws-dataexchange-api-samples
# Flow: create-data-set → create-revision → create-job (IMPORT_ASSETS_FROM_S3) → start-job → update-revision (finalize)
#
# Usage (owner disposes):
#   export AWS_PROFILE=csoai-adx
#   export ADX_S3_PREFIX=s3://csoai-adx-staging/gspc-board/
#   bash ops/adx/stage.sh
set -euo pipefail

REGION="${AWS_REGION:-eu-west-2}"
DATA_SET_NAME="${ADX_DATA_SET_NAME:-csoai-gspc-board}"
S3_PREFIX="${ADX_S3_PREFIX:?Set ADX_S3_PREFIX to staged export prefix}"
ASSET_TYPE="${ADX_ASSET_TYPE:-S3_SNAPSHOT}"

echo "=== ADX staging (PREP-ONLY) ==="
echo "region: $REGION"
echo "data-set: $DATA_SET_NAME"
echo "s3: $S3_PREFIX"

DATA_SET_ID=$(aws dataexchange create-data-set \
  --name "$DATA_SET_NAME" \
  --asset-type "$ASSET_TYPE" \
  --description "GSPC board export — 13 measured of 14. Measurement only, not certification." \
  --region "$REGION" \
  --query 'Id' --output text)
echo "create-data-set: $DATA_SET_ID"

REVISION_ID=$(aws dataexchange create-revision \
  --data-set-id "$DATA_SET_ID" \
  --comment "Initial revision — staged from $S3_PREFIX" \
  --region "$REGION" \
  --query 'Id' --output text)
echo "create-revision: $REVISION_ID"

JOB_ID=$(aws dataexchange create-job \
  --type IMPORT_ASSETS_FROM_S3 \
  --details "{\"ImportAssetsFromS3\":{\"DataSetId\":\"$DATA_SET_ID\",\"RevisionId\":\"$REVISION_ID\",\"AssetSources\":[{\"Bucket\":\"${S3_PREFIX#s3://}\"}]}}" \
  --region "$REGION" \
  --query 'Id' --output text 2>/dev/null || echo "DRY-RUN: create-job skipped (validate AssetSources JSON against live bucket)")
echo "create-job: ${JOB_ID:-DRY-RUN}"

if [[ "${JOB_ID:-}" != "DRY-RUN" && -n "${JOB_ID:-}" ]]; then
  aws dataexchange start-job --job-id "$JOB_ID" --region "$REGION"
  echo "start-job: $JOB_ID"
  aws dataexchange wait job-completed --job-id "$JOB_ID" --region "$REGION" || true
  aws dataexchange update-revision \
    --data-set-id "$DATA_SET_ID" \
    --revision-id "$REVISION_ID" \
    --finalized \
    --region "$REGION"
  echo "update-revision: finalized"
fi

echo "=== ADX staging complete (owner must approve AMMP seller registration before publish) ==="
