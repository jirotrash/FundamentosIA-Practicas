import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

usuario = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")

cliente = MongoClient(f"mongodb+srv://{usuario}:{password}@{cluster}/")
db = cliente[os.getenv("MONGO_DB")]
coleccion = db[os.getenv("MONGO_COLLECTION")]


def guardar():
    nombre = entrada.get().strip()
    if not nombre:
        messagebox.showwarning("Falta dato", "Escribe un nombre")
        return
    coleccion.insert_one({"alumno": nombre})
    entrada.delete(0, tk.END)
    mostrar()


def mostrar():
    lista.delete(0, tk.END)
    for doc in coleccion.find():
        lista.insert(tk.END, doc.get("alumno", "(sin nombre)"))


ventana = tk.Tk()
ventana.title("Mongo + Tkinter")
ventana.geometry("400x350")

tk.Label(ventana, text="Nombre del alumno:").pack(pady=5)

entrada = tk.Entry(ventana, width=30)
entrada.pack()

tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)
tk.Button(ventana, text="Mostrar todos", command=mostrar).pack()

lista = tk.Listbox(ventana, width=45, height=12)
lista.pack(pady=10)

mostrar()
ventana.mainloop()