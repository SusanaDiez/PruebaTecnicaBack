import pytest
from app.services.transaccion_service import TransaccionService
from app.schemas import NotificacionSchema
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError
from app.database import cliente, fondos, transacciones

def setup_function():
    cliente.saldo = 500000
    transacciones.clear()

def test_suscribirse_exitoso():
    notificacion = NotificacionSchema(tipo="email", destinatario="test@example.com")
    resultado = TransaccionService.suscribirse(1, notificacion)
    assert resultado["saldo_restante"] == 425000
    assert len(transacciones) == 1
    assert resultado["transaccion_id"] is not None

def test_suscribirse_fondo_no_encontrado():
    notificacion = NotificacionSchema(tipo="email", destinatario="test@example.com")
    with pytest.raises(FondoNoEncontradoError):
        TransaccionService.suscribirse(999, notificacion)

def test_suscribirse_saldo_insuficiente():
    notificacion = NotificacionSchema(tipo="email", destinatario="test@example.com")
    cliente.saldo = 50000
    with pytest.raises(SaldoInsuficienteError):
        TransaccionService.suscribirse(1, notificacion)

def test_cancelar_exitoso():
    notificacion = NotificacionSchema(tipo="email", destinatario="test@example.com")
    TransaccionService.suscribirse(1, notificacion)
    resultado = TransaccionService.cancelar(1, notificacion)
    assert resultado["saldo_restante"] == 500000
    assert len(transacciones) == 2
    assert resultado["transaccion_id"] is not None

def test_cancelar_fondo_no_encontrado():
    notificacion = NotificacionSchema(tipo="email", destinatario="test@example.com")
    with pytest.raises(FondoNoEncontradoError):
        TransaccionService.cancelar(999, notificacion)
