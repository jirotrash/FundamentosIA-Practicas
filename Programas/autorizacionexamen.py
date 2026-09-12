import tkinter as tk
from tkinter import messagebox

# ==========================================================
# CASO DE ESTUDIO:
# Sistema de autorización para examen
# Versión con interfaz gráfica en Tkinter.
# ==========================================================

ventana = tk.Tk()
ventana.title("Sistema de autorización para examen final")
ventana.geometry("760x620")

tk.Label(ventana, text="SISTEMA DE AUTORIZACIÓN PARA EXAMEN FINAL",
         font=("Arial", 13, "bold")).pack(pady=10)

# ----------------------------------------------------------
# 1. ENTRADA DE DATOS
# ----------------------------------------------------------

marco = tk.Frame(ventana)
marco.pack(pady=5)

tk.Label(marco, text="Porcentaje de asistencia:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
caja_asistencia = tk.Entry(marco, width=10)
caja_asistencia.grid(row=0, column=1, sticky="w")

tk.Label(marco, text="Promedio:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
caja_promedio = tk.Entry(marco, width=10)
caja_promedio.grid(row=1, column=1, sticky="w")

v_proyecto = tk.IntVar()
v_autorizacion = tk.IntVar()
v_adeudos = tk.IntVar()
v_lista = tk.IntVar()

tk.Checkbutton(marco, text="Entregó el proyecto",
               variable=v_proyecto).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
tk.Checkbutton(marco, text="Tiene autorización especial",
               variable=v_autorizacion).grid(row=3, column=0, columnspan=2, sticky="w", padx=5)
tk.Checkbutton(marco, text="Tiene adeudos pendientes",
               variable=v_adeudos).grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
tk.Checkbutton(marco, text="Aparece en la lista de autorizados",
               variable=v_lista).grid(row=5, column=0, columnspan=2, sticky="w", padx=5)

salida = tk.Text(ventana, font=("Courier New", 10), height=22, state="disabled")


def evaluar():
    try:
        asistencia = float(caja_asistencia.get())
        promedio = float(caja_promedio.get())
    except ValueError:
        messagebox.showwarning("Datos inválidos",
                               "La asistencia y el promedio deben ser números.")
        return

    # ------------------------------------------------------
    # 2. CONVERTIMOS LOS DATOS EN PROPOSICIONES
    # ------------------------------------------------------

    P = asistencia >= 80              # asistencia suficiente
    Q = promedio >= 7                 # promedio aprobatorio
    R = v_proyecto.get() == 1         # entregó el proyecto
    S = v_autorizacion.get() == 1     # tiene autorización especial
    T = v_adeudos.get() == 0          # NO tiene adeudos pendientes
    U = v_lista.get() == 1            # aparece en la lista

    # ------------------------------------------------------
    # 3 a 9. OPERACIONES LÓGICAS
    # ------------------------------------------------------

    negacion_P = not P
    conjuncion = P and Q
    disyuncion = Q or S
    condicional = (not P) or Q
    bicondicional = P == Q
    expresion = (P and Q) or S

    resultado_final = expresion and T and U

    # ------------------------------------------------------
    # 10. REPORTE
    # ------------------------------------------------------

    t = []
    t.append("=" * 52)
    t.append(" VALORES DE LAS PROPOSICIONES")
    t.append("=" * 52)
    t.append("P - Asistencia suficiente (>= 80): " + str(P))
    t.append("Q - Promedio aprobatorio (>= 7): " + str(Q))
    t.append("R - Proyecto entregado: " + str(R))
    t.append("S - Autorización especial: " + str(S))
    t.append("T - Sin adeudos pendientes: " + str(T))
    t.append("U - Aparece en la lista: " + str(U))
    t.append("")
    t.append("-" * 52)
    t.append(" OPERACIONES")
    t.append("-" * 52)
    t.append("NEGACIÓN         ¬P = " + str(negacion_P))
    t.append("CONJUNCIÓN     P ∧ Q = " + str(conjuncion))
    t.append("DISYUNCIÓN     Q ∨ S = " + str(disyuncion))
    t.append("CONDICIONAL    P → Q = " + str(condicional))
    t.append("BICONDICIONAL  P ↔ Q = " + str(bicondicional))
    t.append("PARÉNTESIS (P ∧ Q) ∨ S = " + str(expresion))
    t.append("")
    t.append("-" * 52)
    t.append(" RESULTADO")
    t.append("-" * 52)

    if expresion:
        t.append("Requisitos académicos: CUMPLE")
    else:
        t.append("Requisitos académicos: NO CUMPLE")

    t.append("")
    t.append("Decisión final  (P ∧ Q) ∨ S ∧ T ∧ U = " + str(resultado_final))
    t.append("")

    if resultado_final:
        t.append("El alumno PUEDE presentar el examen.")
    else:
        t.append("El alumno NO puede presentar el examen.")
        if not expresion:
            t.append("  Motivo: no cumple asistencia y promedio, ni tiene autorización.")
        if not T:
            t.append("  Motivo: tiene adeudos pendientes.")
        if not U:
            t.append("  Motivo: no aparece en la lista de autorizados.")

    salida.config(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert("1.0", "\n".join(t))
    salida.config(state="disabled")


tk.Button(ventana, text="Evaluar", width=18, command=evaluar).pack(pady=12)
salida.pack(fill="both", expand=True, padx=15, pady=(0, 15))

ventana.mainloop()