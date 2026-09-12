import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

cliente = MongoClient("mongodb://127.0.0.1:27017/", serverSelectionTimeoutMS=5000)
db = cliente["fundamentos"]
coleccion = db["pruebas"]


def guardar():
    texto = entrada.get().strip()
    if not texto:
        messagebox.showwarning("Falta dato", "Escribe un mensaje")
        return
    coleccion.insert_one({"mensaje": texto})
    entrada.delete(0, tk.END)
    mostrar()


def mostrar():
    lista.delete(0, tk.END)
    for doc in coleccion.find():
        lista.insert(tk.END, doc.get("mensaje", "(sin mensaje)"))
    estado.config(text=f"Documentos: {coleccion.count_documents({})}")


def borrar_todo():
    coleccion.delete_many({})
    mostrar()


ventana = tk.Tk()
ventana.title("Mongo local + Tkinter")
ventana.geometry("400x380")

tk.Label(ventana, text="Mensaje:").pack(pady=5)

entrada = tk.Entry(ventana, width=35)
entrada.pack()

tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)
tk.Button(ventana, text="Mostrar todos", command=mostrar).pack()
tk.Button(ventana, text="Borrar todo", command=borrar_todo).pack(pady=5)

lista = tk.Listbox(ventana, width=45, height=12)
lista.pack(pady=5)

estado = tk.Label(ventana, text="")
estado.pack()

try:
    cliente.admin.command("ping")
    mostrar()
except Exception as e:
    messagebox.showerror("Sin conexión", f"No se pudo conectar a MongoDB:\n{e}")

ventana.mainloop()