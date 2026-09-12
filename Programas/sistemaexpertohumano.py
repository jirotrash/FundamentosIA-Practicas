import tkinter as tk
from tkinter import messagebox

# ==========================================================
# SISTEMA EXPERTO DE DIAGNÓSTICO HUMANO BASADO EN REGLAS
# (SIMULACIÓN EDUCATIVA - NO ES UN DIAGNÓSTICO MÉDICO REAL)
# Versión con interfaz gráfica en Tkinter.
# ==========================================================

datos = {}


def si_no(respuesta):
    if respuesta == "s":
        return "Sí"
    else:
        return "No"


def sn(variable):
    """Convierte el valor de un Checkbutton (1/0) a 's'/'n'."""
    if variable.get() == 1:
        return "s"
    else:
        return "n"


ventana = tk.Tk()
ventana.title("Sistema experto de diagnóstico humano")
ventana.geometry("800x720")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True, padx=15, pady=10)


def limpiar():
    for w in contenedor.winfo_children():
        w.destroy()


# ----------------------------------------------------------
# PANTALLA 1: DATOS GENERALES Y SÍNTOMAS (FASE 1)
# ----------------------------------------------------------

def pantalla_uno():
    limpiar()

    tk.Label(contenedor, text="DATOS DEL PACIENTE",
             font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 8))

    campos = {}
    etiquetas = [
        ("nombre", "Nombre:"),
        ("edad", "Edad:"),
        ("peso", "Peso (kg):"),
        ("estatura", "Estatura (cm):"),
        ("sangre", "Tipo de sangre:"),
    ]

    fila = 1
    for clave, texto in etiquetas:
        tk.Label(contenedor, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=2)
        caja = tk.Entry(contenedor, width=22)
        caja.grid(row=fila, column=1, sticky="w")
        campos[clave] = caja
        fila = fila + 1

    v_cronicas = tk.IntVar()
    tk.Checkbutton(contenedor, text="Enfermedades crónicas",
                   variable=v_cronicas).grid(row=fila, column=0, columnspan=2, sticky="w", padx=5)
    e_cronicas = tk.Entry(contenedor, width=28)
    e_cronicas.grid(row=fila, column=2, columnspan=2, sticky="w")
    fila = fila + 1

    v_medicamentos = tk.IntVar()
    tk.Checkbutton(contenedor, text="Toma medicamentos",
                   variable=v_medicamentos).grid(row=fila, column=0, columnspan=2, sticky="w", padx=5)
    e_medicamentos = tk.Entry(contenedor, width=28)
    e_medicamentos.grid(row=fila, column=2, columnspan=2, sticky="w")
    fila = fila + 1

    tk.Label(contenedor, text="FASE 1: SÍNTOMAS GENERALES",
             font=("Arial", 12, "bold")).grid(row=fila, column=0, columnspan=4, pady=(12, 6))
    fila = fila + 1

    sintomas = [
        ("fiebre", "Fiebre"),
        ("tos", "Tos"),
        ("dolor_garganta", "Dolor de garganta"),
        ("dolor_cabeza", "Dolor de cabeza"),
        ("congestion", "Congestión nasal"),
        ("dificultad_respirar", "Dificultad para respirar"),
        ("dolor_muscular", "Dolor muscular"),
        ("cansancio", "Cansancio"),
        ("nauseas", "Náuseas o vómito"),
        ("dolor_abdominal", "Dolor abdominal"),
    ]

    variables = {}
    columna = 0
    for clave, texto in sintomas:
        v = tk.IntVar()
        tk.Checkbutton(contenedor, text=texto, variable=v).grid(
            row=fila, column=columna, columnspan=2, sticky="w", padx=5)
        variables[clave] = v
        if columna == 0:
            columna = 2
        else:
            columna = 0
            fila = fila + 1

    if columna == 2:
        fila = fila + 1

    def continuar():
        # Validación de los datos numéricos.
        try:
            edad = int(campos["edad"].get())
            peso = float(campos["peso"].get())
            estatura = float(campos["estatura"].get())
        except ValueError:
            messagebox.showwarning("Datos inválidos",
                                   "Edad, peso y estatura deben ser números.")
            return

        if estatura <= 0:
            messagebox.showwarning("Datos inválidos", "La estatura debe ser mayor que cero.")
            return

        datos["nombre"] = campos["nombre"].get()
        datos["edad"] = edad
        datos["peso"] = peso
        datos["estatura_cm"] = estatura
        datos["tipo_sangre"] = campos["sangre"].get()

        datos["tiene_cronicas"] = sn(v_cronicas)
        if datos["tiene_cronicas"] == "s":
            datos["cuales_cronicas"] = e_cronicas.get()
        else:
            datos["cuales_cronicas"] = "Ninguna"

        datos["toma_medicamentos"] = sn(v_medicamentos)
        if datos["toma_medicamentos"] == "s":
            datos["cuales_medicamentos"] = e_medicamentos.get()
        else:
            datos["cuales_medicamentos"] = "Ninguno"

        for clave in variables:
            datos[clave] = sn(variables[clave])

        pantalla_dos()

    tk.Button(contenedor, text="Continuar", width=18, command=continuar).grid(
        row=fila, column=0, columnspan=4, pady=15)


# ----------------------------------------------------------
# PANTALLA 2: PROFUNDIZACIÓN (FASE 2)
# ----------------------------------------------------------

def pantalla_dos():
    limpiar()

    # Valores por defecto para las áreas que no se revisan.
    por_defecto = ["flema", "flema_color", "dolor_pecho", "silbidos", "falta_aire",
                   "contacto_enfermo", "placas", "dolor_bajo_derecho", "sangre",
                   "diarrea", "comida_mal_estado", "deshidratacion",
                   "dolor_cabeza_fuerte", "rigidez_cuello", "cansancio_prolongado",
                   "perdida_peso"]
    for clave in por_defecto:
        datos[clave] = "n"
    datos["dias_sintomas"] = 0

    area_respiratoria = (datos["fiebre"] == "s" or datos["tos"] == "s"
                         or datos["dolor_garganta"] == "s" or datos["congestion"] == "s"
                         or datos["dificultad_respirar"] == "s")
    area_digestiva = (datos["nauseas"] == "s" or datos["dolor_abdominal"] == "s")
    area_general = (datos["dolor_cabeza"] == "s" or datos["dolor_muscular"] == "s"
                    or datos["cansancio"] == "s")

    datos["area_respiratoria"] = area_respiratoria
    datos["area_digestiva"] = area_digestiva
    datos["area_general"] = area_general

    # Si no hubo ningún síntoma, se salta directo al reporte.
    if not area_respiratoria and not area_digestiva and not area_general:
        pantalla_tres()
        return

    tk.Label(contenedor, text="FASE 2: PREGUNTAS DE PROFUNDIZACIÓN",
             font=("Arial", 12, "bold")).pack(pady=(0, 10))

    variables = {}
    caja_dias = None

    def bloque(titulo, preguntas):
        marco = tk.LabelFrame(contenedor, text=titulo, padx=10, pady=5)
        marco.pack(fill="x", pady=5)
        for clave, texto in preguntas:
            v = tk.IntVar()
            tk.Checkbutton(marco, text=texto, variable=v).pack(anchor="w")
            variables[clave] = v
        return marco

    if area_respiratoria:
        marco = bloque("Área respiratoria", [
            ("flema", "La tos tiene flema o mucosidad"),
            ("flema_color", "La flema es verde o amarilla"),
            ("dolor_pecho", "Dolor en el pecho al toser o respirar"),
            ("silbidos", "Se escuchan silbidos al respirar"),
            ("falta_aire", "Falta el aire con esfuerzos mínimos"),
            ("contacto_enfermo", "Contacto con alguien enfermo estos días"),
            ("placas", "Manchas blancas en la garganta o dificultad para tragar"),
        ])
        linea = tk.Frame(marco)
        linea.pack(anchor="w", pady=3)
        tk.Label(linea, text="Días con los síntomas:").pack(side="left")
        caja_dias = tk.Entry(linea, width=6)
        caja_dias.insert(0, "0")
        caja_dias.pack(side="left", padx=5)

    if area_digestiva:
        bloque("Área digestiva", [
            ("dolor_bajo_derecho", "El dolor se concentra en la parte baja derecha del abdomen"),
            ("sangre", "Hay sangre en el vómito o en las heces"),
            ("diarrea", "Ha tenido diarrea"),
            ("comida_mal_estado", "Comió algo en mal estado en las últimas 24 horas"),
            ("deshidratacion", "Boca seca, orina poca u oscura, o mareo al levantarse"),
        ])

    if area_general:
        bloque("Área general", [
            ("dolor_cabeza_fuerte", "El dolor de cabeza es el más fuerte de su vida"),
            ("rigidez_cuello", "Rigidez en el cuello junto con la fiebre"),
            ("cansancio_prolongado", "El cansancio lleva más de dos semanas"),
            ("perdida_peso", "Ha perdido peso sin proponérselo"),
        ])

    def ver_diagnostico():
        if caja_dias is not None:
            try:
                datos["dias_sintomas"] = int(caja_dias.get())
            except ValueError:
                messagebox.showwarning("Datos inválidos",
                                       "Los días con síntomas deben ser un número.")
                return

        for clave in variables:
            datos[clave] = sn(variables[clave])

        pantalla_tres()

    tk.Button(contenedor, text="Ver diagnóstico", width=18,
              command=ver_diagnostico).pack(pady=12)


# ----------------------------------------------------------
# MOTOR DE REGLAS
# ----------------------------------------------------------

def evaluar_reglas():
    d = datos

    estatura_m = d["estatura_cm"] / 100
    imc = d["peso"] / (estatura_m * estatura_m)

    if imc < 18.5:
        categoria_imc = "Bajo peso"
    elif imc < 25:
        categoria_imc = "Peso normal"
    elif imc < 30:
        categoria_imc = "Sobrepeso"
    else:
        categoria_imc = "Obesidad"

    p_respiratoria = 0
    p_bacteriana = 0
    p_irritacion = 0
    p_faringitis = 0
    p_resfriado = 0
    p_viral = 0
    p_bronquitis = 0
    p_alergia = 0
    p_digestivo = 0
    p_intoxicacion = 0
    p_nutricional = 0
    p_fatiga = 0
    p_urgencia = 0

    reglas_activadas = []

    # ---------- REGLAS BASE (R-1 a R-14) ----------

    if d["fiebre"] == "s" and d["tos"] == "s":
        reglas_activadas.append(("R-1", "Posible infección respiratoria.", 2))
        p_respiratoria = p_respiratoria + 2

    if d["tos"] == "s" and d["dolor_garganta"] == "s":
        reglas_activadas.append(("R-2", "Posible irritación respiratoria.", 2))
        p_irritacion = p_irritacion + 2

    if d["fiebre"] == "s" and d["dolor_muscular"] == "s" and d["cansancio"] == "s":
        reglas_activadas.append(("R-3", "Posible cuadro viral.", 3))
        p_viral = p_viral + 3

    if d["tos"] == "s" and d["congestion"] == "s":
        reglas_activadas.append(("R-4", "Posible resfriado.", 2))
        p_resfriado = p_resfriado + 2

    if d["dificultad_respirar"] == "s":
        reglas_activadas.append(("R-5", "Se recomienda valoración médica inmediata.", 5))
        p_urgencia = p_urgencia + 5

    if d["dolor_abdominal"] == "s" and d["nauseas"] == "s":
        reglas_activadas.append(("R-6", "Posible cuadro digestivo; se recomienda valoración profesional.", 3))
        p_digestivo = p_digestivo + 3

    if d["edad"] >= 65 and d["fiebre"] == "s":
        reglas_activadas.append(("R-7", "Fiebre en adulto mayor: mayor riesgo de complicaciones.", 3))
        p_urgencia = p_urgencia + 3

    if d["edad"] <= 5 and d["fiebre"] == "s":
        reglas_activadas.append(("R-8", "Fiebre en niño pequeño: requiere valoración médica.", 3))
        p_urgencia = p_urgencia + 3

    if d["tiene_cronicas"] == "s" and (d["fiebre"] == "s" or d["dificultad_respirar"] == "s"):
        reglas_activadas.append(("R-9", "Enfermedad crónica con síntomas activos: mayor riesgo.", 3))
        p_urgencia = p_urgencia + 3

    if imc >= 30 and d["dificultad_respirar"] == "s":
        reglas_activadas.append(("R-10", "La obesidad puede agravar la dificultad respiratoria.", 2))
        p_urgencia = p_urgencia + 2

    if imc < 18.5 and d["cansancio"] == "s":
        reglas_activadas.append(("R-11", "Bajo peso con cansancio: posible déficit nutricional.", 2))
        p_nutricional = p_nutricional + 2

    if d["dolor_cabeza"] == "s" and d["fiebre"] == "s" and d["cansancio"] == "s":
        reglas_activadas.append(("R-12", "Dolor de cabeza con fiebre y cansancio: apoya un cuadro viral.", 2))
        p_viral = p_viral + 2

    if d["congestion"] == "s" and d["dolor_cabeza"] == "s" and d["fiebre"] == "n":
        reglas_activadas.append(("R-13", "Congestión sin fiebre: posible cuadro alérgico o sinusitis.", 2))
        p_alergia = p_alergia + 2

    if d["toma_medicamentos"] == "s" and d["nauseas"] == "s":
        reglas_activadas.append(("R-14", "Las náuseas podrían relacionarse con los medicamentos que toma.", 2))
        p_digestivo = p_digestivo + 2

    # ---------- REGLAS DERIVADAS (FASE 2) ----------

    if d["fiebre"] == "s" and d["dias_sintomas"] >= 4 and d["flema_color"] == "s":
        reglas_activadas.append(("R-1.1", "Fiebre prolongada con flema de color: posible infección bacteriana.", 4))
        p_bacteriana = p_bacteriana + 4

    if d["flema"] == "s" and d["dolor_pecho"] == "s":
        reglas_activadas.append(("R-1.2", "Tos con flema y dolor de pecho: posible bronquitis.", 3))
        p_bronquitis = p_bronquitis + 3

    if d["silbidos"] == "s":
        reglas_activadas.append(("R-1.3", "Silbidos al respirar: posible componente asmático o alérgico.", 3))
        p_alergia = p_alergia + 3

    if d["falta_aire"] == "s":
        reglas_activadas.append(("R-1.4", "Falta de aire con esfuerzos mínimos: signo de alarma.", 5))
        p_urgencia = p_urgencia + 5

    if d["contacto_enfermo"] == "s" and d["fiebre"] == "s":
        reglas_activadas.append(("R-1.5", "Contacto con persona enferma y fiebre: posible contagio viral.", 2))
        p_viral = p_viral + 2

    if 0 < d["dias_sintomas"] <= 3 and d["congestion"] == "s" and d["fiebre"] == "n":
        reglas_activadas.append(("R-1.6", "Pocos días, con congestión y sin fiebre: apoya un resfriado común.", 2))
        p_resfriado = p_resfriado + 2

    if d["placas"] == "s" and d["dolor_garganta"] == "s":
        reglas_activadas.append(("R-2.1", "Manchas blancas en garganta: posible faringitis bacteriana.", 4))
        p_faringitis = p_faringitis + 4

    if d["dolor_bajo_derecho"] == "s":
        reglas_activadas.append(("R-6.1", "Dolor en parte baja derecha del abdomen: posible apendicitis.", 5))
        p_urgencia = p_urgencia + 5

    if d["sangre"] == "s":
        reglas_activadas.append(("R-6.2", "Sangre en vómito o heces: señal de alarma digestiva.", 5))
        p_urgencia = p_urgencia + 5

    if d["diarrea"] == "s" and d["nauseas"] == "s":
        reglas_activadas.append(("R-6.3", "Diarrea con náuseas: posible gastroenteritis.", 3))
        p_digestivo = p_digestivo + 3

    if d["comida_mal_estado"] == "s":
        reglas_activadas.append(("R-6.4", "Consumo de alimento en mal estado: posible intoxicación alimentaria.", 3))
        p_intoxicacion = p_intoxicacion + 3

    if d["deshidratacion"] == "s":
        reglas_activadas.append(("R-6.5", "Signos de deshidratación: requiere atención.", 3))
        p_urgencia = p_urgencia + 3

    if d["dolor_cabeza_fuerte"] == "s":
        reglas_activadas.append(("R-3.1", "Dolor de cabeza nunca antes sentido: alarma neurológica.", 5))
        p_urgencia = p_urgencia + 5

    if d["rigidez_cuello"] == "s" and d["fiebre"] == "s":
        reglas_activadas.append(("R-3.2", "Rigidez de cuello con fiebre: signo de alarma.", 5))
        p_urgencia = p_urgencia + 5

    if d["cansancio_prolongado"] == "s":
        reglas_activadas.append(("R-3.3", "Cansancio de más de dos semanas: conviene estudiarlo.", 2))
        p_fatiga = p_fatiga + 2

    if d["perdida_peso"] == "s":
        reglas_activadas.append(("R-3.4", "Pérdida de peso sin proponérselo: conviene estudiarlo.", 3))
        p_fatiga = p_fatiga + 3

    if len(reglas_activadas) == 0:
        reglas_activadas.append(("R-0", "No se identificó un patrón específico.", 0))

    puntajes = [
        ["Posible infección respiratoria", p_respiratoria],
        ["Posible infección bacteriana respiratoria", p_bacteriana],
        ["Posible irritación respiratoria", p_irritacion],
        ["Posible faringitis bacteriana", p_faringitis],
        ["Posible resfriado común", p_resfriado],
        ["Posible cuadro viral", p_viral],
        ["Posible bronquitis", p_bronquitis],
        ["Posible componente alérgico o asmático", p_alergia],
        ["Posible cuadro digestivo (gastroenteritis)", p_digestivo],
        ["Posible intoxicación alimentaria", p_intoxicacion],
        ["Posible déficit nutricional", p_nutricional],
        ["Posible fatiga o pérdida de peso a estudiar", p_fatiga],
        ["Situación que requiere valoración médica inmediata", p_urgencia],
    ]

    mejor_diagnostico = "No se identificó un patrón específico."
    mejor_puntaje = 0
    for nombre_diagnostico, puntos in puntajes:
        if puntos > mejor_puntaje:
            mejor_puntaje = puntos
            mejor_diagnostico = nombre_diagnostico

    return imc, categoria_imc, reglas_activadas, puntajes, mejor_diagnostico, mejor_puntaje, p_urgencia


# ----------------------------------------------------------
# PANTALLA 3: REPORTE FINAL
# ----------------------------------------------------------

def armar_texto():
    d = datos
    imc, categoria_imc, reglas, puntajes, mejor, mejor_puntaje, p_urgencia = evaluar_reglas()

    t = []
    t.append("=" * 52)
    t.append("          REPORTE DE DIAGNÓSTICO")
    t.append("=" * 52)
    t.append("")
    t.append("DATOS DEL PACIENTE")
    t.append("")
    t.append("Nombre: " + d["nombre"])
    t.append("Edad: " + str(d["edad"]) + " años")
    t.append("Peso: " + str(d["peso"]) + " kg")
    t.append("Estatura: " + str(d["estatura_cm"]) + " cm")
    t.append("Tipo de sangre: " + d["tipo_sangre"])

    if d["tiene_cronicas"] == "s":
        t.append("Enfermedades crónicas: Sí (" + d["cuales_cronicas"] + ")")
    else:
        t.append("Enfermedades crónicas: No")

    if d["toma_medicamentos"] == "s":
        t.append("Medicamentos: Sí (" + d["cuales_medicamentos"] + ")")
    else:
        t.append("Medicamentos: No")

    t.append("")
    t.append("-" * 52)
    t.append("SÍNTOMAS (FASE 1)")
    t.append("-" * 52)
    t.append("")
    t.append("Fiebre: " + si_no(d["fiebre"]))
    t.append("Tos: " + si_no(d["tos"]))
    t.append("Dolor de garganta: " + si_no(d["dolor_garganta"]))
    t.append("Dolor de cabeza: " + si_no(d["dolor_cabeza"]))
    t.append("Congestión nasal: " + si_no(d["congestion"]))
    t.append("Dificultad para respirar: " + si_no(d["dificultad_respirar"]))
    t.append("Dolor muscular: " + si_no(d["dolor_muscular"]))
    t.append("Cansancio: " + si_no(d["cansancio"]))
    t.append("Náuseas o vómito: " + si_no(d["nauseas"]))
    t.append("Dolor abdominal: " + si_no(d["dolor_abdominal"]))

    t.append("")
    t.append("-" * 52)
    t.append("PROFUNDIZACIÓN (FASE 2)")
    t.append("-" * 52)
    t.append("")

    if d["area_respiratoria"]:
        t.append("Área respiratoria:")
        t.append("  Días con síntomas: " + str(d["dias_sintomas"]))
        t.append("  Tos con flema: " + si_no(d["flema"]))
        t.append("  Flema verde o amarilla: " + si_no(d["flema_color"]))
        t.append("  Dolor en el pecho: " + si_no(d["dolor_pecho"]))
        t.append("  Silbidos al respirar: " + si_no(d["silbidos"]))
        t.append("  Falta de aire con esfuerzo mínimo: " + si_no(d["falta_aire"]))
        t.append("  Contacto con persona enferma: " + si_no(d["contacto_enfermo"]))
        t.append("  Manchas blancas en garganta: " + si_no(d["placas"]))

    if d["area_digestiva"]:
        t.append("Área digestiva:")
        t.append("  Dolor en parte baja derecha: " + si_no(d["dolor_bajo_derecho"]))
        t.append("  Sangre en vómito o heces: " + si_no(d["sangre"]))
        t.append("  Diarrea: " + si_no(d["diarrea"]))
        t.append("  Alimento en mal estado: " + si_no(d["comida_mal_estado"]))
        t.append("  Signos de deshidratación: " + si_no(d["deshidratacion"]))

    if d["area_general"]:
        t.append("Área general:")
        t.append("  Dolor de cabeza nunca antes sentido: " + si_no(d["dolor_cabeza_fuerte"]))
        t.append("  Rigidez en el cuello: " + si_no(d["rigidez_cuello"]))
        t.append("  Cansancio de más de dos semanas: " + si_no(d["cansancio_prolongado"]))
        t.append("  Pérdida de peso involuntaria: " + si_no(d["perdida_peso"]))

    if not d["area_respiratoria"] and not d["area_digestiva"] and not d["area_general"]:
        t.append("No fue necesario profundizar: no se reportaron síntomas.")

    t.append("")
    t.append("-" * 52)
    t.append("IMC")
    t.append("-" * 52)
    t.append("")
    t.append("IMC: " + str(round(imc, 2)) + " - " + categoria_imc)

    t.append("")
    t.append("-" * 52)
    t.append("REGLAS ACTIVADAS")
    t.append("-" * 52)
    t.append("")
    for codigo, mensaje, puntos in reglas:
        t.append(codigo + " -> " + mensaje + " (+" + str(puntos) + ")")

    t.append("")
    t.append("-" * 52)
    t.append("PUNTAJE POR DIAGNÓSTICO")
    t.append("-" * 52)
    t.append("")
    hubo_puntos = False
    for nombre_diagnostico, puntos in puntajes:
        if puntos > 0:
            t.append(nombre_diagnostico + ": " + str(puntos) + " puntos")
            hubo_puntos = True
    if not hubo_puntos:
        t.append("Ningún diagnóstico acumuló puntos.")

    t.append("")
    t.append("-" * 52)
    t.append("RESULTADO")
    t.append("-" * 52)
    t.append("")
    t.append(mejor + " (" + str(mejor_puntaje) + " puntos)")

    if p_urgencia > 0:
        t.append("")
        t.append("ALERTA:")
        t.append("Se detectaron signos que requieren valoración médica pronta.")

    t.append("")
    t.append("RECOMENDACIÓN:")
    if p_urgencia >= 5:
        t.append("Acude a valoración médica de inmediato o a urgencias.")
    else:
        t.append("Se recomienda valoración por un profesional de la salud")
        t.append("para confirmar el diagnóstico.")

    t.append("")
    t.append("=" * 52)
    t.append("Este resultado es una simulación educativa y")
    t.append("NO sustituye un diagnóstico médico real.")
    t.append("=" * 52)

    return "\n".join(t)


def pantalla_tres():
    limpiar()

    tk.Label(contenedor, text="REPORTE DE DIAGNÓSTICO",
             font=("Arial", 12, "bold")).pack(pady=(0, 5))

    marco = tk.Frame(contenedor)
    marco.pack(fill="both", expand=True)

    barra = tk.Scrollbar(marco)
    barra.pack(side="right", fill="y")

    texto = tk.Text(marco, font=("Courier New", 10), yscrollcommand=barra.set)
    texto.pack(fill="both", expand=True)
    barra.config(command=texto.yview)

    texto.insert("1.0", armar_texto())
    texto.config(state="disabled")

    tk.Button(contenedor, text="Nuevo diagnóstico", width=20,
              command=pantalla_uno).pack(pady=10)


# ----------------------------------------------------------
# AVISO Y ARRANQUE
# ----------------------------------------------------------

aviso = tk.Label(ventana,
                 text="SIMULACIÓN EDUCATIVA - NO ES UN DIAGNÓSTICO MÉDICO REAL",
                 fg="white", bg="#b03a2e", font=("Arial", 10, "bold"))
aviso.pack(side="bottom", fill="x")

pantalla_uno()
ventana.mainloop()