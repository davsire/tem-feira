from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://temfeira:{password}@cluster0.nyra0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)

db = client.TemFeira
collection_clientes = db.clientes
collection_feirantes = db.feirantes

doc = {"_id": 0,"nome": "davi", "Tem": "Feira"}

def insert_clientes_doc(doc):
    inserted_id = collection_clientes.insert_one(doc).inserted_id

def insert_feirantes_doc(doc):
    inserted_id = collection_feirantes.insert_one(doc).inserted_id

def achar_cliente_id(cliente_id):
    _id = ObjectId(cliente_id)
    cliente = collection_clientes.find_one({"_id": _id})
    return cliente

def achar_feirante_id(feirante_id):
    _id = ObjectId(feirante_id)
    feirante = collection_feirantes.find_one({"_id": _id})
    return feirante

def update_cliente_id(cliente_id):
    _id = ObjectId(cliente_id)

    update = {
        "$set": {"": ""}
    }
    collection_clientes.update_one({"_id": _id}, update)

def replace_cliente(cliente_id):
    _id = ObjectId(cliente_id)

    new_doc = {
        "": ""
    }

    collection_clientes.replace_one({"_id": _id}, new_doc)

def delete_cliente(cliente_id):
    _id = ObjectId(cliente_id)

    collection_clientes.delete_one({"_id": _id})
