import random

from datetime import datetime

numero = random.randint(1, 100)

numero_reporte = " R " + str(numero)

fecha_hora = datetime.now()

#formato de fecha y hora
fecha_hora_formateada = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")

#hora
hora = fecha_hora.strftime("%H:%M:%S")