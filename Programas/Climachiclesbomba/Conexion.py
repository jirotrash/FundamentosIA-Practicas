"""Conexión a MongoDB Atlas y operaciones CRUD sobre la colección."""

import os

import streamlit as st
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


@st.cache_resource
def obtener_coleccion():
    """Una sola conexión para toda la sesión (no se reabre en cada rerun)."""
    usuario = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    cluster = os.getenv("MONGO_CLUSTER")
    cliente = MongoClient(f"mongodb+srv://{usuario}:{password}@{cluster}/")
    return cliente[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]


def insertar(documento):
    return obtener_coleccion().insert_one(documento).inserted_id


def consultar(filtro=None):
    """Devuelve los registros, del más reciente al más antiguo."""
    return list(obtener_coleccion().find(filtro or {}).sort("fecha", -1))


def modificar(id_registro, cambios):
    return obtener_coleccion().update_one(
        {"_id": ObjectId(id_registro)}, {"$set": cambios}
    ).modified_count


def borrar(id_registro):
    return obtener_coleccion().delete_one(
        {"_id": ObjectId(id_registro)}
    ).deleted_count