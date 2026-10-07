# Image Upscaler API & Background Remover (Batch 2x/4x) — Apify Actor usage guide

[![Run on Apify](https://img.shields.io/badge/Apify-Run%20this%20Actor-24C1E0)](https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara)
[![Try Apify free](https://img.shields.io/badge/Apify-Try%20it%20free-24C1E0)](https://console.apify.com/sign-up?fpr=aupara)

Image upscaler API: batch upscale images 2x/4x and remove backgrounds from image URLs or datasets with open models on CPU. Returns PNG/WebP/JPEG links, sizes and status per image. From $1 per 1,000 images.

> **This repository does not contain the Actor's source code.** The Actor is closed-source and
> runs on Apify's infrastructure. This repo is documentation plus ready-to-run client examples
> (curl, Python, JavaScript) that call the hosted Actor with **your own** Apify API token.

**Run it on Apify →** [https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara](https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara)

## What it does

For every image URL it downloads the image, then runs one of three modes:

- **upscale** – enlarge 2x or 4x with a Real-ESRGAN model (`realesr-general-x4v3`, BSD-3-Clause).
- **remove-background** – transparent cut-out with U2-Net (`u2netp`, Apache-2.0).
- **both** – cut out the background, then enlarge the result.

The processed image is saved in the run's key-value store, and the dataset row holds its public URL and metadata.

## Use cases

- Batch upscale 2x or 4x low-resolution product photos from a list of image URLs
- Remove the background of product photos to transparent PNG (or white background JPEG) for marketplaces
- Upscale and cut out in one run (mode 'both') for catalogue clean-up
- Pipe the image URLs scraped by another Actor (dataset id + field name) straight into a clean-up step
- Prepare larger, cleaner images for datasets or print-on-demand mockups


## Input

| Field | Type | Required | Description |
|---|---|---|---|
| `imageUrls` | array | no | Public http(s) URLs of JPEG, PNG or WebP images. Use this and/or a dataset below. |
| `datasetId` | string | no | ID of an Apify dataset whose rows contain image URLs (for example the output of a product scraper). |
| `datasetUrlField` | string | no | Field holding the image URL; dot paths allowed (e.g. images.0). A field containing an array of URLs is expanded. |
| `mode` | string | no | upscale: enlarge. remove-background: transparent cut-out. both: cut-out then enlarge. |
| `scale` | integer | no | 2 or 4 (ignored for remove-background). |
| `outputFormat` | string | no | Transparency needs png or webp; jpeg is flattened onto the background colour (white by default). |
| `backgroundColor` | string | no | Optional hex colour such as #ffffff to replace transparency after background removal. |
| `maxInputMegapixels` | number | no | Larger inputs are downscaled (or rejected, see below) to bound time and cost. 0.1 to 4. |
| `downscaleLargeInputs` | boolean | no | If off, images above the megapixel limit return an unbilled TOO_LARGE row. |
| `maxResults` | integer | no | Process at most this many images (also caps your spending). |
| `maxConcurrency` | integer | no | Keep low: processing is CPU and memory heavy. |
| `proxyConfiguration` | object | no | Optional. Only needed if the image host blocks direct requests; datacenter proxy was enough in testing. |

The full input form (with defaults and validation) is on the [Actor page](https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara).


## Output (sample item)

Sample trimmed for readability (long texts and lists are shortened) — a real run returns the complete data.

```json
{
  "inputUrl": "https://commons.wikimedia.org/wiki/Special:FilePath/Cat_November_2010-1a.jpg?width=400",
  "status": "success",
  "mode": "upscale",
  "scale": 2,
  "outputUrl": "https://api.apify.com/v2/key-value-stores/UHdyMw0qMkTZqjODP/records/img-0001.png",
  "outputKey": "img-0001.png",
  "outputFormat": "png",
  "inputWidth": 500,
  "inputHeight": 668,
  "outputWidth": 1000,
  "outputHeight": 1336,
  "wasDownscaled": false,
  "outputBytes": 2717428,
  "processingMs": 6394,
  "models": [
    "realesr-general-x4v3 (BSD-3-Clause)"
  ],
  "errorCode": null,
  "errorMessage": null,
  "processedAt": "2026-10-05T21:55:49.815Z"
}
```

## Pricing

Pay only for results: about **$1.50 per 1,000 results** on the Apify Free plan, down to **$1.00 per 1,000** on paid Apify plans.

Apify platform usage (compute) is billed by Apify on top of the per-result price — about **$2.17 per 1,000 results** in our measured test runs (estimate, varies with input). Tip: keep only the output formats and options you need to reduce it.

Prices can change — the [Actor page](https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara) always shows the current pricing.

## Quick start

You need an Apify account and an API token (Apify Console → **Settings → API & Integrations**).
Never commit your token: export it as the `APIFY_TOKEN` environment variable.

### cURL

```bash
curl -X POST "https://api.apify.com/v2/acts/leadsbrary~image-upscaler-background-remover-onnx/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
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
```

### Python (`apify-client`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
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

run = client.actor("leadsbrary/image-upscaler-background-remover-onnx").call(run_input=run_input)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### JavaScript (`apify-client`)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const runInput = {
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
};

const run = await client.actor('leadsbrary/image-upscaler-background-remover-onnx').call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable versions live in [`examples/`](./examples).

## Troubleshooting

- **401 / "User was not found or authentication token is not valid"** — check that `APIFY_TOKEN` is set and copied completely.
- **The run finished but the dataset is empty** — widen your search input or check the run log on the Apify Console.
- **Run stops early** — you may have reached the maximum cost per run you set in Apify; raise it in the run options.
- **Need something else?** Open an issue in this repository or use the Issues tab on the Actor page.

## Don't have an Apify account yet?

[Sign up here](https://console.apify.com/sign-up?fpr=aupara) — new accounts get $5 of free platform usage every month, enough to try most Actors without paying upfront.
Browse the full [Apify Store](https://apify.com/store?fpr=aupara) or [all Actors from this developer](https://apify.com/leadsbrary?fpr=aupara).

## Links

- Actor page: [https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara](https://apify.com/leadsbrary/image-upscaler-background-remover-onnx?fpr=aupara)
- All Actors from this developer: [https://apify.com/leadsbrary?fpr=aupara](https://apify.com/leadsbrary?fpr=aupara)
- Apify API reference: [https://docs.apify.com/api/v2](https://docs.apify.com/api/v2)

## Keywords

image upscaler api, batch image upscaler, ai image upscaler, upscale image 4x, real-esrgan upscaler, background remover api, remove background from image, transparent png background removal, bulk background remover, product photo enhancer, image super resolution, u2net background removal, e-commerce image processing

#ImageUpscaler #BackgroundRemover #RealESRGAN #AIImage #Ecommerce #ProductPhotos #ImageProcessing #ONNX #Automation

## License

The example code in this repository is released under the MIT License — see [LICENSE](./LICENSE).
It does not cover the Actor itself, which remains closed-source and is operated by its developer on Apify.
