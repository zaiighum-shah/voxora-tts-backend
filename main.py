import os
import tempfile
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Voxora TTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

VOICES = [
    {"id":"en-US-AriaNeural","name":"Aria","gender":"Female","accent":"American"},
    {"id":"en-US-JennyNeural","name":"Jenny","gender":"Female","accent":"American"},
    {"id":"en-US-SaraNeural","name":"Sara","gender":"Female","accent":"American"},
    {"id":"en-US-MichelleNeural","name":"Michelle","gender":"Female","accent":"American"},
    {"id":"en-US-AnaNeural","name":"Ana","gender":"Female","accent":"American"},
    {"id":"en-US-EmmaNeural","name":"Emma","gender":"Female","accent":"American"},
    {"id":"en-US-AvaNeural","name":"Ava","gender":"Female","accent":"American"},
    {"id":"en-US-AndrewNeural","name":"Andrew","gender":"Male","accent":"American"},
    {"id":"en-US-BrianNeural","name":"Brian","gender":"Male","accent":"American"},
    {"id":"en-US-GuyNeural","name":"Guy","gender":"Male","accent":"American"},
    {"id":"en-US-ChristopherNeural","name":"Christopher","gender":"Male","accent":"American"},
    {"id":"en-US-EricNeural","name":"Eric","gender":"Male","accent":"American"},
    {"id":"en-GB-SoniaNeural","name":"Sonia","gender":"Female","accent":"British"},
    {"id":"en-GB-LibbyNeural","name":"Libby","gender":"Female","accent":"British"},
    {"id":"en-GB-MaisieNeural","name":"Maisie","gender":"Female","accent":"British"},
    {"id":"en-GB-RyanNeural","name":"Ryan","gender":"Male","accent":"British"},
    {"id":"en-GB-ThomasNeural","name":"Thomas","gender":"Male","accent":"British"},
    {"id":"en-AU-NatashaNeural","name":"Natasha","gender":"Female","accent":"Australian"},
    {"id":"en-AU-WilliamNeural","name":"William","gender":"Male","accent":"Australian"},
    {"id":"en-IN-NeerjaNeural","name":"Neerja","gender":"Female","accent":"Indian"},
    {"id":"en-IN-PrabhatNeural","name":"Prabhat","gender":"Male","accent":"Indian"},
]

class GenerateRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    format: str = "mp3"

@app.get("/")
def health():
    return {"status":"ok","service":"Voxora TTS API"}

@app.get("/voices")
def voices():
    return {"voices": VOICES}

@app.post("/generate")
async def generate(req: GenerateRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    if req.voice not in {v["id"] for v in VOICES}:
        raise HTTPException(status_code=400, detail="Invalid voice")
    if req.format.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 is supported")

    speed = max(0.5, min(req.speed, 2.0))
    rate = f"{int((speed - 1) * 100):+d}%"
    pitch = f"{int(req.pitch):+d}Hz"

    fd, output = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    try:
        await edge_tts.Communicate(
            req.text, req.voice, rate=rate, pitch=pitch
        ).save(output)
        return FileResponse(output, media_type="audio/mpeg", filename="voxora.mp3")
    except Exception as e:
        if os.path.exists(output):
            os.remove(output)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
