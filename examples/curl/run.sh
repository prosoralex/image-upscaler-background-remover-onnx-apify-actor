#!/usr/bin/env bash
# Run the "Image Upscaler API & Background Remover (Batch 2x/4x)" Apify Actor synchronously and print the dataset items.
# Usage: export APIFY_TOKEN=your_apify_token && ./run.sh
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN first (Apify Console > Settings > API & Integrations)}"

curl -sS -X POST "https://api.apify.com/v2/acts/leadsbrary~image-upscaler-background-remover-onnx/run-sync-get-dataset-items" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "imageUrls": [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Cat_November_2010-1a.jpg?width=400",
    "https://picsum.photos/id/10/400/300.jpg"
  ],
  "datasetUrlField": "imageUrl",
  "mode": "upscale",
  "scale": 2,
  "outputFormat": "png",
  "maxInputMegapixels": 0.5,
  "downscaleLargeInputs": true,
  "maxResults": 2,
  "maxConcurrency": 1,
  "proxyConfiguration": {
    "useApifyProxy": false
  }
}
JSON
