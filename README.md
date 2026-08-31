# Voxora TTS Backend

A small FastAPI backend for Voxora's voice studio. It exposes:

- `GET /` health/status
- `GET /health`
- `GET /voices`
- `POST /generate` → MP3

## Important: free TTS engine

This version uses `edge-tts`, which accesses Microsoft's Edge online neural TTS service without an API key. It is convenient for a zero-budget prototype, but it is **not an official Microsoft Azure API** and it is not an unlimited commercial SLA. For a product you plan to sell, consider switching the provider later to an official paid/contracted TTS API.

## Deploy on Railway

1. Create an Empty Service in Railway.
2. Put this backend in a GitHub repository.
3. In Railway, choose **Deploy from GitHub Repo** for the service, or connect the repo to the service.
4. Railway detects the Dockerfile automatically.
5. After deployment, open the generated public domain.
6. Test:
   - `/`
   - `/voices`
7. Set your frontend `config.js` `tts.baseUrl` to the Railway URL, for example:
   `https://your-service.up.railway.app`

## CORS

By default this backend allows all origins for easy testing. For production, set Railway environment variable:

`ALLOWED_ORIGINS=https://your-real-domain.example`

For GitHub Pages, use your exact Pages origin.

## Frontend integration

The existing Voxora frontend sends:

```json
{
  "text": "Hello world",
  "voice": "en-US-AriaNeural",
  "accent": "American English",
  "speed": 1,
  "pitch": 1,
  "volume": 1,
  "format": "mp3"
}
```

The response is `audio/mpeg`.

## Character length

The API intentionally has no 5,000-character UI limit. Long scripts are split into smaller chunks and stitched into one MP3. Extremely large jobs can still hit provider/network/resource limits, so "unlimited" should not be advertised as literally unlimited.

## Security

Do not put private provider/API keys in frontend JavaScript. If you later add a paid provider, keep its secret key in Railway environment variables.
