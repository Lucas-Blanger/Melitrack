from fastapi import APIRouter

app = APIRouter()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ml"}
