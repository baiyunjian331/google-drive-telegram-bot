import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot import LOGGER
from bot.runner import start_bot, stop_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_bot()
    try:
        yield
    finally:
        # Give Pyrogram a short moment to flush pending tasks before shutting down
        await asyncio.sleep(0.1)
        await stop_bot()


api = FastAPI(title="Google Drive Uploader Bot", lifespan=lifespan)
# Alias expected by some deployment platforms (e.g. Hugging Face Spaces)
app = api


@api.get("/")
async def root() -> dict:
    return {"status": "running", "message": "Google Drive Telegram Bot is active."}


@api.get("/healthz")
async def healthcheck() -> dict:
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    LOGGER.info("Starting FastAPI server for Hugging Face deployment.")
    uvicorn.run(
        "app:api",
        host="0.0.0.0",
        port=int(7860),
        reload=False,
        log_level="info",
    )
