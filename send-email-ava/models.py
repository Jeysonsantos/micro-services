from pydantic import BaseModel


class DetailEmail(BaseModel):
    email: str
    title: str
    message: str
