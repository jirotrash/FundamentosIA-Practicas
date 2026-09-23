"""Agente Reactivo Simple de Climatización — Tkinter + MongoDB Atlas."""

import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

usuario = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")

cliente = MongoClient(f"mongodb+srv://{usuario}:{password}@{cluster}/")
db = cliente[os.getenv("MONGO_DB")]
coleccion = db[os.getenv("MONGO_COLLECTION")]


def tomar_decision(temperatura, humedad):
    """Regla condición-acción del agente."""
    if temperatura > 30 and humedad > 70:
        return "Encender aire acondicionado (Modo Deshumidificador)"
    if temperatura > 30:
        return "Encender ventilador"
    if temperatura < 18:
        return "Encender calefacción"
    return "Mantener sistema apagado"


def procesar():
    """Percibe lo capturado en la ventana, decide y guarda en MongoDB."""
    try:
        temperatura = float(entrada_temp.get().replace(",", "."))
        humedad = float(entrada_hum.get().replace(",", "."))
    except ValueError:
        estado.config(text="Ingresa números válidos.", foreground="red")
        return

    accion = tomar_decision(temperatura, humedad)
    etiqueta_accion.config(text=f"Acción -> {accion}")

    try:
        coleccion.insert_one({
            "temperatura": temperatura,
            "humedad": humedad,
            "accion": accion,
            "fecha": datetime.now(),
        })
        estado.config(text="Guardado en MongoDB.", foreground="green")
    except Exception as error:
        estado.config(text=f"Error al guardar: {error}", foreground="red")


ventana = tk.Tk()
ventana.title("Agente de Climatización")
marco = ttk.Frame(ventana, padding=20)
marco.pack()

ttk.Label(marco, text="Temperatura (°C):").grid(row=0, column=0, sticky="w", pady=4)
entrada_temp = ttk.Entry(marco)
entrada_temp.grid(row=0, column=1, pady=4)

ttk.Label(marco, text="Humedad (%):").grid(row=1, column=0, sticky="w", pady=4)
entrada_hum = ttk.Entry(marco)
entrada_hum.grid(row=1, column=1, pady=4)

ttk.Button(marco, text="Evaluar y guardar", command=procesar).grid(
    row=2, column=0, columnspan=2, pady=12
)

etiqueta_accion = ttk.Label(marco, text="Acción -> (sin evaluar)", wraplength=320)
etiqueta_accion.grid(row=3, column=0, columnspan=2)

estado = ttk.Label(marco, text="", foreground="gray")
estado.grid(row=4, column=0, columnspan=2, pady=(6, 0))

ventana.mainloop()