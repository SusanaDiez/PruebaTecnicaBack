class Cliente:
    def __init__(self, saldo: float):
        self.saldo = saldo

cliente = Cliente(saldo=500000)

fondos = [
    {"id": 1, "nombre": "FPV_BTG_PACTUAL_RECAUDADORA", "monto_minimo": 75000, "categoria": "FPV"},
    {"id": 2, "nombre": "FPV_BTG_PACTUAL_ECOPETROL", "monto_minimo": 125000, "categoria": "FPV"},
    {"id": 3, "nombre": "DEUDAPRIVADA", "monto_minimo": 50000, "categoria": "FIC"},
    {"id": 4, "nombre": "FDO-ACCIONES", "monto_minimo": 250000, "categoria": "FIC"},
    {"id": 5, "nombre": "FPV_BTG_PACTUAL_DINAMICA", "monto_minimo": 100000, "categoria": "FPV"}
]

transacciones = []
