from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import DetailEmail

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send_email/")
async def send_email(detail_email: DetailEmail):

    print(detail_email)

    return {"message": "Email has been sent successfully"}


#inicializar - uvicorn main:app --reload --port 8002

