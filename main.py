from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
# client = MongoClient("mongodb://<usuario>:<contraseña>@157.253.236.88:8087")

#client = MongoClient("mongodb://ISIS2304C13202610:o6uTVZGK0Fz9@157.253.236.88:8087/")
# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS*******"]
db = client["ISIS2304C13202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/proveedores')
def get_proveedores():
    return list(db["proveedores"].find({}, {'_id': 0}))

@app.get('/proveedores/{proveedor_id}')
def get_proveedor_bebida(bebida_id: int):
    proveedor = db["proveedores"].find_one({"bebidas_suministradas": bebida_id}, {'_id': 0})
    return proveedor or {}

@app.post('/proveedores')
def post_proveedor(datos: dict):
    datos['fecha_registro'] = datetime.now().isoformat()
    db["proveedores"].insert_one(datos)
    return {'mensaje': 'Proveedor registrado'}

@app.put('/proveedores/{nombre}')
def update_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].replace_one({"nombre": nombre}, datos)
    return {'mensaje': 'Proveedor actualizado correctamente'}

@app.patch('/proveedores/{nombre}')
def patch_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].update_one({"nombre": nombre}, {"$set": datos})
    return {'mensaje': 'Campos actualizados correctamente'}

@app.delete('/proveedores/{nombre}')
def delete_proveedor(nombre: str):
    resultado = db["proveedores"].delete_one({"nombre": nombre})
    return {'mensaje': f'Proveedor {nombre} eliminado correctamente'}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios"].find({"bar_id": bar_id}, {'_id': 0}))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    # TODO: completar
    db["comentarios"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find({"bar_id": bar_id}, {'_id': 0}))
    return eventos

# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento registrado'}