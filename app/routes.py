from fastapi import APIRouter, HTTPException

from app.database import transacciones
from app.services.transaccion_service import TransaccionService
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError
from app.database import cliente

router = APIRouter()

@router.get("/saldo")
def saldo():
    return cliente.saldo

@router.post("/suscribirse")
def suscribirse(fondo_id: int, tipo: str, destinatario: str):
    try:
        resultado = TransaccionService.suscribirse(fondo_id, tipo, destinatario)
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
def cancelar(fondo_id: int, tipo: str, destinatario: str):
    try:
        resultado = TransaccionService.cancelar(fondo_id, tipo, destinatario)
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
