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


def insert_clientes_doc(doc):
    if achar_usuario(doc["email"]) is None:
        return collection_clientes.insert_one(doc).inserted_id

def insert_feirantes_doc(doc):
    if achar_usuario(doc["email"]) is None:
        return collection_feirantes.insert_one(doc).inserted_id

def achar_cliente_id(cliente_id):
    return collection_clientes.find_one({"_id": ObjectId(cliente_id)})

def achar_feirante_id(feirante_id):
    return collection_feirantes.find_one({"_id": ObjectId(feirante_id)})

def achar_usuario(email):
    return collection_clientes.find_one({"email": email}) or collection_feirantes.find_one({"email": email})

def update_cliente(cliente_id, info):

    update = {
        "$set": { "email": info["email"], 
                  "senha": info["senha"], 
                  "nome": info["nome"], 
                  "localizacao": info["localizacao"]
                }
    }
    collection_clientes.update_one({"_id": ObjectId(cliente_id)}, update)

def update_feirante(feirante_id, info):

    update = {
        "$set": { "email": info["email"], 
                  "senha": info["senha"], 
                  "nome": info["nome"], 
                  "localizacao": info["localizacao"]
                }
    }
    collection_feirantes.update_one({"_id": ObjectId(feirante_id)}, update)

def delete_cliente(cliente_id):
    collection_clientes.delete_one({"_id": ObjectId(cliente_id)})

def delete_feirante(feirante_id):
    collection_feirantes.delete_one({"_id": ObjectId(feirante_id)})

def create_feirantes_collection():
    feirante_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "EMAIL", 
                "senha", 
                "nome_feira", 
                "dia_da_semana", 
                "horario_abertura", 
                "horario_fechamento", 
                "localizacao", 
                "forma_contato", 
                "contato", 
                "produtos"
            ],
            "properties": {
                "EMAIL": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "senha": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "nome_feira": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "dias_de_funcionamento": {
                    "bsonType": "array",
                    "description": "must be an array and is required",
                    "items": {
                        "bsonType": "object",
                        "required": [
                            "dia", 
                            "horario_abertura", 
                            "horario_fechamento"
                        ],
                        "properties": {
                            "dia": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "horario_abertura": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "horario_fechamento": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        }
                    }
                },
                "localizacao": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "forma_contato": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "contato": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "produtos": {
                    "bsonType": "array",
                    "description": "must be an array and is required",
                    "items": {
                        "bsonType": "object",
                        "required": [
                            "nome", 
                            "preco", 
                            "imagem", 
                            "quantidade", 
                            "unidade"
                        ],
                        "properties": {
                            "produto_id": {
                                "bsonType": "objectId",
                                "description": "must be an objectId and is required"
                            },
                            "nome": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "preco": {
                                "bsonType": "number",
                                "description": "must be a number and is required"
                            },
                            "imagem": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "quantidade": {
                                "bsonType": "number",
                                "description": "must be a number and is required"
                            },
                            "unidade": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        }
                    }
                }
            }
        }
    }

    try:
        db.create_collection("feirantes")
    except Exception as e:
        print(e)
    
    db.command("collMod", "feirantes", validator=feirante_validator)

def create_clientes_collection():
    clientes_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "EMAIL", 
                "senha", 
                "nome", 
                "localizacao"
            ],
            "properties": {
                "EMAIL": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "senha": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "nome": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "localizacao": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }
    
    try:
        db.create_collection("clientes")
    except Exception as e:
        print(e)
    
    db.command("collMod", "clientes", validator=clientes_validator)
