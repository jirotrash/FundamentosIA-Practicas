import tkinter as tk
from tkinter import messagebox
import ttg


def generar():
    variables = [v.strip() for v in entrada_vars.get().split(",") if v.strip()]
    expresiones = [e.strip() for e in entrada_exprs.get().split(",") if e.strip()]

    if not variables:
        messagebox.showwarning("Falta dato", "Escribe al menos una variable")
        return

    try:
        tabla = ttg.Truths(variables, expresiones, ints=False)
    except Exception as e:
        messagebox.showerror("Error", f"Revisa tus expresiones:\n{e}")
        return

    salida.config(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, str(tabla))
    salida.config(state="disabled")


ventana = tk.Tk()
ventana.title("Tablas de verdad")
ventana.geometry("700x450")

tk.Label(ventana, text="Variables (separadas por coma):").pack(pady=(10, 0))
entrada_vars = tk.Entry(ventana, width=60)
entrada_vars.insert(0, "p, q")
entrada_vars.pack()

tk.Label(ventana, text="Expresiones (separadas por coma):").pack(pady=(10, 0))
entrada_exprs = tk.Entry(ventana, width=60)
entrada_exprs.insert(0, "not p, p and q, p or q, p => q, p = q")
entrada_exprs.pack()

tk.Button(ventana, text="Generar tabla", command=generar).pack(pady=10)

salida = tk.Text(ventana, font=("Courier New", 11), height=15, state="disabled")
salida.pack(fill="both", expand=True, padx=10, pady=10)

generar()
ventana.mainloop()  