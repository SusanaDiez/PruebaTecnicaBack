from datetime import datetime
from uuid import uuid4
from app.database import cliente, fondos, transacciones
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError
from app.utils import enviar_email, enviar_sms
import logging

logger = logging.getLogger(__name__)

class TransaccionService:

    @staticmethod
    def suscribirse(fondo_id: int, tipo: str, destinatario: str):
        fondo = next((f for f in fondos if f["id"] == fondo_id), None)
        if not fondo:
            raise FondoNoEncontradoError(f"Fondo con id {fondo_id} no encontrado")

        if cliente.saldo < fondo["monto_minimo"]:
            raise SaldoInsuficienteError(f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}")

        cliente.saldo -= fondo["monto_minimo"]
        transaccion_id = str(uuid4())
        transaccion = {
            "id": transaccion_id,
            "fondo_id": fondo_id,
            "tipo": "suscripcion",
            "fecha": datetime.now(),
        }
        transacciones.append(transaccion)

        mensaje = f"Suscripción exitosa al fondo {fondo['nombre']}. ID de transacción: {transaccion_id}"

        try:
            if tipo == "email":  #notificacion.tipo == "email":
                enviar_email(destinatario, "Suscripción de Fondo", mensaje)
            elif tipo == "sms":  #notificacion.tipo == "sms":
                enviar_sms(destinatario, mensaje)
        except RuntimeError as e:
            logger.error(f"Error al enviar notificación: {e}")

        return {"mensaje": mensaje, "saldo_restante": cliente.saldo, "transaccion_id": transaccion_id}

    @staticmethod
    def cancelar(fondo_id: int, tipo: str, destinatario: str):
        fondo = next((f for f in fondos if f["id"] == fondo_id), None)
        if not fondo:
            raise FondoNoEncontradoError(f"Fondo con id {fondo_id} no encontrado")

        transaccion = next((t for t in transacciones if t["fondo_id"] == fondo_id and t["tipo"] == "suscripcion"), None)
        if not transaccion:
            raise FondoNoEncontradoError(f"No hay suscripción activa para el fondo con id {fondo_id}")

        cliente.saldo += fondo["monto_minimo"]
        transaccion_cancelacion = {
            "id": str(uuid4()),
            "fondo_id": fondo_id,
            "tipo": "cancelacion",
            "fecha": datetime.now(),
        }
        transacciones.append(transaccion_cancelacion)

        mensaje = f"Cancelada la suscripción al fondo {fondo['nombre']}. ID de transacción: {transaccion_cancelacion['id']}"

        try:
            if tipo == "email":
                enviar_email(destinatario, "Cancelación de Suscripción", mensaje)
            elif tipo == "sms":
                enviar_sms(destinatario, mensaje)
        except RuntimeError as e:
            logger.error(f"Error al enviar notificación: {e}")

        return {"mensaje": mensaje, "saldo_restante": cliente.saldo, "transaccion_id": transaccion_cancelacion["id"]}
