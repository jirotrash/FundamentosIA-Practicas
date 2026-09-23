"""Agente Reactivo Simple de Climatización: percepción -> decisión -> acción."""

from datetime import datetime

ACCIONES = [
    "Encender aire acondicionado (Modo Deshumidificador)",
    "Encender ventilador",
    "Encender calefacción",
    "Mantener sistema apagado",
]


class AgenteClimatizacion:
    def __init__(self):
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""

    def percibir(self, temperatura, humedad):
        """Recibe los datos del entorno."""
        self.temperatura = float(temperatura)
        self.humedad = float(humedad)

    def tomar_decision(self):
        """Aplica la regla condición-acción basada en la percepción."""
        if self.temperatura > 30 and self.humedad > 70:
            self.accion = ACCIONES[0]
        elif self.temperatura > 30:
            self.accion = ACCIONES[1]
        elif self.temperatura < 18:
            self.accion = ACCIONES[2]
        else:
            self.accion = ACCIONES[3]
        return self.accion

    def a_documento(self):
        """Arma el documento que se guarda en MongoDB."""
        return {
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "accion": self.accion,
            "fecha": datetime.now(),
        }