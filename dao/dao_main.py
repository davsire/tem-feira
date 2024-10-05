import os
import json
from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


class DaoMain(ABC):

    def __init__(self):
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        connection_string = f"mongodb+srv://temfeira:{password}@cluster0.nyra0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(connection_string)
        self.db = client.get_database('TemFeira')

    @abstractmethod
    def obter_nome_collection(self) -> str:
        pass

    def find(self, query):
        self.db.get_collection(self.obter_nome_collection()).find(query)

    def find_one(self, query):
        self.db.get_collection(self.obter_nome_collection()).find_one(query)

    def insert_one(self, documento):
        self.db.get_collection(self.obter_nome_collection()).insert_one(documento)

    def update_one(self, query, documento):
        update = {
            "$set": documento
        }
        self.db.get_collection(self.obter_nome_collection()).update_one(query, update)

    def delete_one(self, query):
        self.db.get_collection(self.obter_nome_collection()).delete_one(query)

    def criar_collection_feirantes(self):
        with open('./assets/feirante_validator.json') as feirante_validator_file:
            feirante_validator = json.load(feirante_validator_file)

        try:
            self.db.create_collection("feirantes")
        except Exception as e:
            print(e)

        self.db.command("collMod", "feirantes", validator=feirante_validator)

    def criar_collection_clientes(self):
        with open('./assets/cliente_validator.json') as cliente_validator_file:
            cliente_validator = json.load(cliente_validator_file)

        try:
            self.db.create_collection("clientes")
        except Exception as e:
            print(e)

        self.db.command("collMod", "clientes", validator=cliente_validator)
