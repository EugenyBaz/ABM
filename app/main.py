from fastapi import FastAPI


app = FastAPI(title="ABM-AsyncBridgeManager")

@app.get("/health")
async def health_check():
    return {"status": "ok"}