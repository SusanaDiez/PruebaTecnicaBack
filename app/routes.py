from fastapi import APIRouter, HTTPException

from app.database import transacciones
from app.services.transaccion_service import TransaccionService
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError
from app.notifications import Notification
from app.database import cliente

router = APIRouter()

@router.get("/saldo")
def saldo():
    return cliente.saldo

@router.post("/suscribirse")
def suscribirse(request: Notification):
    try:
        resultado = TransaccionService.suscribirse(request.dict())
        return resultado
    except FondoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SaldoInsuficienteError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cancelar")
def cancelar(request: Notification):
    try:
        resultado = TransaccionService.cancelar(request.dict())
        return resultado
    except FondoNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transacciones")
def listar_transacciones():
    return transacciones
