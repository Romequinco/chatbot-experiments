from fastapi import FastAPI
from app.webhook import router

app = FastAPI(title="WhatsApp Chatbot")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
