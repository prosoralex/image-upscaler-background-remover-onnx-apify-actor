"""
Run the "Image Upscaler API & Background Remover (Batch 2x/4x)" Apify Actor and print its results.

Setup:
    pip install -r requirements.txt
    export APIFY_TOKEN=your_apify_token   # Apify Console > Settings > API & Integrations

This repository only documents the Actor; its source code runs on Apify's infrastructure.
"""
import os
import sys

from apify_client import ApifyClient

ACTOR_ID = "leadsbrary/image-upscaler-background-remover-onnx"

RUN_INPUT = {
    "imageUrls": [
        "https://commons.wikimedia.org/wiki/Special:FilePath/Cat_November_2010-1a.jpg?width=400",
        "https://picsum.photos/id/10/400/300.jpg"
    ],
    "datasetUrlField": "imageUrl",
    "mode": "upscale",
    "scale": 2,
    "outputFormat": "png",
    "maxInputMegapixels": 0.5,
    "downscaleLargeInputs": True,
    "maxResults": 2,
    "maxConcurrency": 1,
    "proxyConfiguration": {
        "useApifyProxy": False
    }
}


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    print(f"Starting {ACTOR_ID} ...")
    run = client.actor(ACTOR_ID).call(run_input=RUN_INPUT)
    print(f"Run finished with status: {run['status']}")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)


if __name__ == "__main__":
    main()
