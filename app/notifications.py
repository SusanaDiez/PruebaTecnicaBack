from pydantic import BaseModel

class Notification(BaseModel):
    fondo_id: int
    tipo: str
    destinatario: str
