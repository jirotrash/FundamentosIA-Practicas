"""Interfaz Streamlit: CRUD y clasificador del agente de climatización."""

import pandas as pd
import streamlit as st

from Agente import ACCIONES, AgenteClimatizacion
from Conexion import borrar, consultar, insertar, modificar


def cargar(filtro=None):
    """Consulta MongoDB y devuelve los registros como DataFrame."""
    registros = consultar(filtro)
    if not registros:
        return pd.DataFrame(
            columns=["_id", "fecha", "temperatura", "humedad", "accion"]
        )
    datos = pd.DataFrame(registros)
    datos["_id"] = datos["_id"].astype(str)
    return datos


def etiquetar(fila):
    """Texto descriptivo de un registro, tolerante a campos faltantes."""
    fecha = fila.get("fecha")
    texto_fecha = "sin fecha" if pd.isna(fecha) else f"{fecha:%d/%m/%Y %H:%M}"
    return (
        f"{texto_fecha} — {fila.get('temperatura', '-')}°C / "
        f"{fila.get('humedad', '-')}% — {fila.get('accion', '-')}"
    )


st.set_page_config(page_title="Agente de Climatización", layout="wide")
st.title("Agente Reactivo Simple de Climatización")

pestañas = st.tabs(["Registrar", "Registros", "Clasificador"])

# ------------------------------ CREATE --------------------------------
with pestañas[0]:
    st.subheader("Nueva lectura")
    with st.form("form_crear"):
        columna1, columna2 = st.columns(2)
        temperatura = columna1.number_input("Temperatura (°C)", value=25.0, step=0.5)
        humedad = columna2.number_input("Humedad (%)", value=50.0, step=1.0)
        enviado = st.form_submit_button("Evaluar y guardar")

    if enviado:
        agente = AgenteClimatizacion()
        agente.percibir(temperatura, humedad)
        accion = agente.tomar_decision()
        insertar(agente.a_documento())
        st.success(f"Acción -> {accion}")

# --------------------- READ / UPDATE / DELETE -------------------------
with pestañas[1]:
    st.subheader("Registros guardados")
    datos = cargar()

    if datos.empty:
        st.info("Todavía no hay lecturas registradas.")
    else:
        st.dataframe(
            datos[["fecha", "temperatura", "humedad", "accion"]],
            hide_index=True,
            width="stretch",
        )

        st.divider()
        st.subheader("Editar o eliminar")

        opciones = {etiquetar(fila): fila["_id"] for _, fila in datos.iterrows()}
        etiqueta = st.selectbox("Selecciona un registro", list(opciones))
        id_elegido = opciones[etiqueta]
        actual = datos[datos["_id"] == id_elegido].iloc[0]

        columna1, columna2 = st.columns(2)
        nueva_temp = columna1.number_input(
            "Temperatura (°C)",
            value=float(actual["temperatura"]) if pd.notna(actual["temperatura"]) else 25.0,
            step=0.5,
            key="upd_t",
        )
        nueva_hum = columna2.number_input(
            "Humedad (%)",
            value=float(actual["humedad"]) if pd.notna(actual["humedad"]) else 50.0,
            step=1.0,
            key="upd_h",
        )

        boton1, boton2 = st.columns(2)
        if boton1.button("Actualizar", width="stretch"):
            agente = AgenteClimatizacion()
            agente.percibir(nueva_temp, nueva_hum)
            accion = agente.tomar_decision()
            modificar(id_elegido, {
                "temperatura": agente.temperatura,
                "humedad": agente.humedad,
                "accion": accion,
            })
            st.success(f"Registro actualizado -> {accion}")
            st.rerun()

        if boton2.button("Eliminar", type="primary", width="stretch"):
            borrar(id_elegido)
            st.warning("Registro eliminado.")
            st.rerun()

# ---------------------------- CLASIFICADOR ----------------------------
with pestañas[2]:
    st.subheader("Clasificador de lecturas")

    elegida = st.selectbox("Clasificar por acción", ["Todas"] + ACCIONES)
    filtro = None if elegida == "Todas" else {"accion": elegida}
    clasificados = cargar(filtro)

    st.caption(f"{len(clasificados)} registro(s) en esta clase.")

    if clasificados.empty:
        st.info("No hay registros para este filtro.")
    else:
        st.dataframe(
            clasificados[["fecha", "temperatura", "humedad", "accion"]],
            hide_index=True,
            width="stretch",
        )

        if elegida == "Todas":
            st.bar_chart(clasificados["accion"].value_counts())
        else:
            cronologico = clasificados.dropna(subset=["fecha"]).sort_values("fecha")
            if cronologico.empty:
                st.info("Estos registros no tienen fecha para graficar en el tiempo.")
            else:
                st.line_chart(
                    cronologico.set_index("fecha")[["temperatura", "humedad"]]
                )