import tkinter as tk
from tkinter import messagebox

# ==========================================================
# SISTEMA DE DIAGNÓSTICO DE DISPOSITIVOS
# Versión con interfaz gráfica en Tkinter.
# ==========================================================

# ----------------------------------------------------------
# 1. CHECKLIST DE ENCENDIDO
# ----------------------------------------------------------
# Cada pregunta trae: texto, respuesta que confirma la causa
# (si/no), la causa y en qué dispositivos aplica.

PREGUNTAS_ENCENDIDO = [
    ("¿El tomacorriente o multicontacto tiene corriente confirmada con otro aparato?",
     "no", "El problema es la instalación eléctrica o el enchufe.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿El cargador o cable de corriente entrega el voltaje correcto sin falsos contactos?",
     "no", "El eliminador o cable de corriente está dañado.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿El switch trasero de la fuente de poder (I/O) está en posición de encendido (\"I\")?",
     "no", "No entra corriente a la fuente de poder.",
     {"pc", "servidor"}),
    ("¿El equipo enciende si retiras completamente la batería y usas solo el cargador?",
     "si", "La batería interna está en corto y bloquea la carga.",
     {"laptop"}),
    ("¿El pin de carga (jack DC) está firme y sin juego mecánico?",
     "no", "El conector interno de carga está desoldado o roto.",
     {"laptop", "tablet"}),

    ("¿El botón de encendido hace el \"clic\" físico habitual y manda señal a la placa?",
     "no", "El switch está roto o el cable del panel frontal está desconectado.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿La placa madre o la fuente emiten olor a quemado o tienen condensadores inflados?",
     "si", "Daño irreversible en la circuitería o cortocircuito directo.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿El equipo prende uno o dos segundos y se apaga de inmediato en bucle?",
     "si", "Cortocircuito en la línea de 12V, procesador mal asentado o pines doblados.",
     {"pc", "laptop", "servidor"}),
    ("¿Hacer un puente directo en los pines PWR_SW de la tarjeta madre enciende el equipo?",
     "si", "El botón de encendido del gabinete está defectuoso.",
     {"pc", "servidor"}),
    ("¿La pila de botón (CR2032) de la BIOS tiene carga suficiente (más de 2.8V)?",
     "no", "Placas antiguas no completan el ciclo de encendido sin batería CMOS.",
     {"pc", "laptop", "servidor"}),

    ("¿El equipo enciende normalmente si desconectas absolutamente todo lo que esté en los puertos USB?",
     "si", "Un puerto USB roto o un periférico conectado está haciendo tierra/corto.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿El disipador del procesador está bien ajustado y con la pasta térmica en buen estado?",
     "no", "Protección térmica por sobrecalentamiento apaga el equipo al arrancar.",
     {"pc", "laptop", "servidor"}),
    ("¿Se quitó recientemente algún componente que pueda haber dejado suciedad o polvo en los contactos?",
     "si", "Se requiere limpieza con alcohol isopropílico en los zócalos.",
     {"pc", "laptop", "servidor", "tablet"}),

    ("¿El equipo enciende si lo sacas del gabinete de metal y lo armas sobre una mesa o caja de cartón?",
     "si", "Un tornillo o poste separador del gabinete está tocando las pistas de la placa base.",
     {"pc", "servidor"}),
    ("¿El equipo enciende al desconectar TODOS los discos duros, SSDs SATA y unidades M.2?",
     "si", "Una unidad de almacenamiento o su cable de corriente interno está en corto.",
     {"pc", "laptop", "servidor"}),
    ("Si tienes un extensor de tarjeta de video (riser), ¿enciende si conectas la gráfica directo a la placa base sin el cable?",
     "si", "El cable extensor (riser) está roto o hay conflicto de versiones de PCIe.",
     {"pc", "servidor"}),
    ("¿Enciende si desconectas el teclado interno directamente desde la placa base?",
     "si", "El teclado sufrió daño por humedad y está bloqueando el encendido.",
     {"laptop"}),

    ("¿Al retirar el procesador, se observa algún pin doblado en el zócalo o debajo del CPU?",
     "si", "Se pierde la comunicación con la RAM o el chipset, impidiendo el POST.",
     {"pc", "laptop", "servidor"}),
    ("¿Aflojar un poco los tornillos del disipador permite que el equipo encienda?",
     "si", "Había demasiada presión física deformando la placa, separando los pines del procesador.",
     {"pc", "laptop", "servidor"}),
    ("¿Se ven manchas blancas, sarro verde o zonas pegajosas cerca de los disipadores de la placa madre?",
     "si", "Daño por humedad o líquidos que carcomió las pistas de los reguladores de voltaje.",
     {"pc", "laptop", "servidor"}),
    ("¿Al desconectar el cable de energía del procesador (4 u 8 pines), la PC intenta arrancar aunque no dé video?",
     "si", "Los reguladores de voltaje (Mosfets) del procesador están quemados y en cortocircuito.",
     {"pc", "servidor"}),

    ("¿El equipo dejó de encender o dar video justo después de una actualización, una pantalla azul o un corte de luz?",
     "si", "El firmware/BIOS se corrompió (equipo \"brickeado\"). Requiere reprogramación.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿La pantalla permanece negra pero reacciona si pasas un imán pequeño por el borde del teclado o de la pantalla?",
     "si", "El sensor magnético de tapa (Sensor Hall) se quedó pegado; el equipo \"cree\" que sigue cerrado.",
     {"laptop", "tablet"}),
    ("¿El equipo prende medio segundo y se apaga con un sonido de \"clic\" metálico dentro de la fuente de poder?",
     "si", "La fuente detecta una anomalía crítica y activa su relé de protección.",
     {"pc", "servidor"}),
]

# ----------------------------------------------------------
# 2. CHECKLIST DE VIDEO / POST
# ----------------------------------------------------------

PREGUNTAS_VIDEO = [
    ("¿Giran los ventiladores o prenden los LEDs de la placa, pero la pantalla sigue negra?",
     "si", "Falla de inicialización de CPU, RAM o GPU.",
     {"pc", "laptop", "servidor"}),
    ("¿El equipo emite pitidos con el buzzer o enciende un LED de depuración (CPU/DRAM/VGA)?",
     "si", "La placa base identifica el componente exacto que falló.",
     {"pc", "laptop", "servidor"}),
    ("¿El equipo logra encender si retiras todos los módulos de RAM y pruebas solo uno por uno?",
     "si", "Uno de los módulos de RAM o una ranura (slot) está dañado.",
     {"pc", "laptop", "servidor"}),
    ("¿Al conectar a un monitor externo mediante HDMI se ve imagen?",
     "si", "El flex de la pantalla o el panel LCD interno está roto.",
     {"laptop"}),
    ("¿El cable de video (HDMI/DisplayPort) está conectado directo a la tarjeta gráfica y no a la placa?",
     "no", "Si tu CPU no tiene gráficos integrados, no dará video por la placa.",
     {"pc", "servidor"}),
]

# ----------------------------------------------------------
# 3. CHECKLIST DE DISCO / ALMACENAMIENTO
# ----------------------------------------------------------

PREGUNTAS_DISCO = [
    ("¿El disco aparece listado en la BIOS/UEFI?",
     "no", "El disco no está siendo detectado por la placa; puede estar dañado o mal conectado.",
     {"pc", "laptop", "servidor"}),
    ("¿El cable de datos SATA está bien conectado en ambos extremos?",
     "no", "El cable de datos SATA está suelto o dañado.",
     {"pc", "laptop", "servidor"}),
    ("¿El cable de alimentación (power) del disco está conectado?",
     "no", "El disco no está recibiendo alimentación eléctrica.",
     {"pc", "servidor"}),
    ("¿El disco se salió físicamente de su ranura o bahía?",
     "si", "El disco está mal asentado, reinsértalo en su ranura.",
     {"laptop", "tablet"}),
    ("¿Al conectar el disco en otra computadora o mediante un adaptador USB se detecta y lee con normalidad?",
     "no", "El disco está dañado físicamente (falla mecánica o electrónica).",
     {"pc", "laptop", "servidor"}),
    ("¿La controladora RAID marca alguno de los discos del arreglo como failed u offline?",
     "si", "Uno de los discos del arreglo RAID falló; reemplázalo y reconstruye el arreglo.",
     {"servidor"}),
    ("¿El almacenamiento interno dejó de reconocerse justo después de una actualización de firmware o una caída de energía?",
     "si", "El firmware del almacenamiento interno (eMMC/UFS) se corrompió; requiere reflasheo especializado.",
     {"tablet"}),
]

# ----------------------------------------------------------
# 4. CHECKLIST DE SISTEMA OPERATIVO
# ----------------------------------------------------------

PREGUNTAS_SO = [
    ("¿El disco aparece como dispositivo de arranque en el orden de arranque (boot order)?",
     "no", "El orden de arranque está mal configurado o el disco no tiene una partición booteable.",
     {"pc", "laptop", "servidor"}),
    ("¿Aparece un mensaje como \"No bootable device\" o \"Operating system not found\"?",
     "si", "El sistema operativo no está instalado o la tabla de particiones (MBR/GPT) está dañada.",
     {"pc", "laptop", "servidor"}),
    ("¿El equipo llega a mostrar el logo de la marca pero se queda ahí sin avanzar?",
     "si", "El gestor de arranque (bootloader) o archivos críticos del sistema están corruptos.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿Se realizó una actualización del sistema, instalación de software o hubo un corte de luz durante un arranque reciente?",
     "si", "La actualización o instalación quedó incompleta y dañó el sistema operativo.",
     {"pc", "laptop", "servidor", "tablet"}),
    ("¿El equipo reconoce una unidad USB booteable al intentar iniciar desde ella?",
     "no", "Hay un problema de hardware (puerto USB o configuración de arranque) más allá del sistema operativo.",
     {"pc", "laptop", "servidor"}),
    ("¿El dispositivo entra en modo de recuperación al mantener presionados los botones de volumen y encendido?",
     "si", "El sistema operativo está dañado, pero puede reinstalarse desde el modo de recuperación.",
     {"tablet"}),
]

# Preguntas principales: texto, checklist que se abre si la
# respuesta es "no", y el título del área revisada.
PRINCIPALES = [
    ("¿Enciende el dispositivo?", PREGUNTAS_ENCENDIDO, "Encendido"),
    ("¿Se ve la imagen?", PREGUNTAS_VIDEO, "Video / POST"),
    ("¿Tiene disco duro?", PREGUNTAS_DISCO, "Disco / Almacenamiento"),
    ("¿Tiene sistema operativo?", PREGUNTAS_SO, "Sistema operativo"),
]

OPCIONES = {
    "1": "pc",
    "2": "laptop",
    "3": "servidor",
    "4": "tablet",
}

reporte = {}
contador_reportes = [0]

# ----------------------------------------------------------
# VENTANA
# ----------------------------------------------------------

ventana = tk.Tk()
ventana.title("Sistema de diagnóstico técnico")
ventana.geometry("720x560")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True, padx=20, pady=15)


def limpiar():
    for w in contenedor.winfo_children():
        w.destroy()


# ----------------------------------------------------------
# PANTALLA 1: DATOS Y DISPOSITIVO
# ----------------------------------------------------------

def pantalla_datos():
    limpiar()

    tk.Label(contenedor, text="SISTEMA DE DIAGNÓSTICO TÉCNICO",
             font=("Arial", 14, "bold")).pack(pady=(0, 15))

    marco = tk.Frame(contenedor)
    marco.pack()

    campos = {}
    etiquetas = [("usuario", "Nombre de usuario:"),
                 ("nombre", "Nombre completo:"),
                 ("direccion", "Dirección:")]

    fila = 0
    for clave, texto in etiquetas:
        tk.Label(marco, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=4)
        caja = tk.Entry(marco, width=30)
        caja.grid(row=fila, column=1, sticky="w")
        campos[clave] = caja
        fila = fila + 1

    tk.Label(contenedor, text="¿Qué dispositivo quieres diagnosticar?",
             font=("Arial", 11, "bold")).pack(pady=(20, 5))

    eleccion = tk.StringVar(value="1")
    for numero in ["1", "2", "3", "4"]:
        tk.Radiobutton(contenedor, text=OPCIONES[numero].capitalize(),
                       variable=eleccion, value=numero).pack(anchor="center")

    def iniciar():
        if campos["usuario"].get().strip() == "":
            messagebox.showwarning("Falta dato", "Escribe el nombre de usuario.")
            return

        contador_reportes[0] = contador_reportes[0] + 1

        reporte.clear()
        reporte["numero"] = str(contador_reportes[0])
        reporte["usuario"] = campos["usuario"].get()
        reporte["nombre"] = campos["nombre"].get()
        reporte["direccion"] = campos["direccion"].get()
        reporte["dispositivo"] = OPCIONES[eleccion.get()]
        reporte["bitacora"] = []
        reporte["causa"] = None
        reporte["area"] = None

        pantalla_preguntas()

    tk.Button(contenedor, text="Iniciar diagnóstico", width=20,
              command=iniciar).pack(pady=25)


# ----------------------------------------------------------
# PANTALLA 2: PREGUNTAS UNA POR UNA
# ----------------------------------------------------------

estado = {}


def pantalla_preguntas():
    limpiar()

    estado["modo"] = "principal"      # "principal" o "checklist"
    estado["indice"] = 0              # posición en PRINCIPALES
    estado["lista"] = []              # checklist filtrada por dispositivo
    estado["pos"] = 0                 # posición dentro de la checklist

    etiqueta_area = tk.Label(contenedor, text="", font=("Arial", 11, "bold"), fg="#1a5276")
    etiqueta_area.pack(pady=(10, 5))

    etiqueta_pregunta = tk.Label(contenedor, text="", font=("Arial", 12),
                                 wraplength=620, justify="left")
    etiqueta_pregunta.pack(pady=20)

    marco_botones = tk.Frame(contenedor)
    marco_botones.pack(pady=10)

    def filtrar(preguntas):
        """Deja solo las preguntas que aplican al dispositivo elegido."""
        lista = []
        for pregunta, respuesta_causa, causa, dispositivos in preguntas:
            if reporte["dispositivo"] in dispositivos:
                lista.append((pregunta, respuesta_causa, causa))
        return lista

    def mostrar():
        if estado["modo"] == "principal":
            etiqueta_area.config(text="Revisión general")
            texto = PRINCIPALES[estado["indice"]][0]
        else:
            etiqueta_area.config(text="Revisando: " + estado["area"]
                                 + "  (" + str(estado["pos"] + 1)
                                 + " de " + str(len(estado["lista"])) + ")")
            texto = estado["lista"][estado["pos"]][0]
        etiqueta_pregunta.config(text=texto)

    def responder(respuesta):
        if estado["modo"] == "principal":
            pregunta, preguntas, area = PRINCIPALES[estado["indice"]]
            reporte["bitacora"].append((pregunta, respuesta))

            if respuesta == "no":
                # Se abre la checklist de esa área.
                estado["area"] = area
                reporte["area"] = area
                estado["lista"] = filtrar(preguntas)
                estado["pos"] = 0
                estado["modo"] = "checklist"

                if len(estado["lista"]) == 0:
                    pantalla_reporte()
                    return
                mostrar()
                return

            # Respondió "si": pasa a la siguiente pregunta principal.
            estado["indice"] = estado["indice"] + 1
            if estado["indice"] >= len(PRINCIPALES):
                reporte["area"] = "Ninguna"
                reporte["causa"] = "sin_fallas"
                pantalla_reporte()
                return
            mostrar()
            return

        # Modo checklist.
        pregunta, respuesta_causa, causa = estado["lista"][estado["pos"]]
        reporte["bitacora"].append((pregunta, respuesta))

        if respuesta == respuesta_causa:
            reporte["causa"] = causa
            pantalla_reporte()
            return

        estado["pos"] = estado["pos"] + 1
        if estado["pos"] >= len(estado["lista"]):
            pantalla_reporte()
            return
        mostrar()

    tk.Button(marco_botones, text="Sí", width=12,
              command=lambda: responder("si")).pack(side="left", padx=10)
    tk.Button(marco_botones, text="No", width=12,
              command=lambda: responder("no")).pack(side="left", padx=10)

    mostrar()


# ----------------------------------------------------------
# PANTALLA 3: REPORTE
# ----------------------------------------------------------

def armar_texto():
    t = []
    t.append("=" * 55)
    t.append("               DATOS DEL REPORTE")
    t.append("=" * 55)
    t.append("Número de reporte : " + reporte["numero"])
    t.append("Usuario           : " + reporte["usuario"])
    t.append("Nombre            : " + reporte["nombre"])
    t.append("Dirección         : " + reporte["direccion"])
    t.append("Dispositivo       : " + reporte["dispositivo"])
    t.append("")
    t.append("=" * 55)
    t.append("               DIAGNÓSTICO")
    t.append("=" * 55)
    t.append("")

    if reporte["causa"] == "sin_fallas":
        t.append("El/la " + reporte["dispositivo"] + " funciona correctamente.")
        t.append("No se detectaron fallas.")
    elif reporte["causa"] is not None:
        t.append("Área revisada: " + str(reporte["area"]))
        t.append("")
        t.append("Causa identificada:")
        t.append("  - " + reporte["causa"])
    else:
        t.append("Área revisada: " + str(reporte["area"]))
        t.append("")
        t.append("No se identificó una causa específica con las revisiones anteriores.")
        t.append("Se recomienda llevar el equipo a servicio técnico especializado.")

    t.append("")
    t.append("-" * 55)
    t.append("RESPUESTAS REGISTRADAS")
    t.append("-" * 55)
    t.append("")
    for pregunta, respuesta in reporte["bitacora"]:
        if respuesta == "si":
            marca = "Sí"
        else:
            marca = "No"
        t.append("[" + marca + "] " + pregunta)

    t.append("")
    t.append("=" * 55)
    t.append("Reporte generado: " + reporte["numero"])
    t.append("=" * 55)

    return "\n".join(t)


def pantalla_reporte():
    limpiar()

    tk.Label(contenedor, text="REPORTE DE DIAGNÓSTICO",
             font=("Arial", 13, "bold")).pack(pady=(0, 8))

    marco = tk.Frame(contenedor)
    marco.pack(fill="both", expand=True)

    barra = tk.Scrollbar(marco)
    barra.pack(side="right", fill="y")

    texto = tk.Text(marco, font=("Courier New", 10), wrap="word", yscrollcommand=barra.set)
    texto.pack(fill="both", expand=True)
    barra.config(command=texto.yview)

    texto.insert("1.0", armar_texto())
    texto.config(state="disabled")

    tk.Button(contenedor, text="Nuevo diagnóstico", width=20,
              command=pantalla_datos).pack(pady=10)


pantalla_datos()
ventana.mainloop()