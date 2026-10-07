// Run the "Image Upscaler API & Background Remover (Batch 2x/4x)" Apify Actor and print its results.
// Setup: npm install  &&  export APIFY_TOKEN=your_apify_token  &&  node example.mjs
// This repository only documents the Actor; its source code runs on Apify's infrastructure.
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
    process.exit(1);
}

const client = new ApifyClient({ token });

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
console.log(`Run finished with status: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(JSON.stringify(items, null, 2));
