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
        return self.db.get_collection(self.obter_nome_collection()).find(query)

    def find_one(self, query):
        return self.db.get_collection(self.obter_nome_collection()).find_one(query)

    def insert_one(self, documento):
        return self.db.get_collection(self.obter_nome_collection()).insert_one(documento)

    def update_one(self, query, update):
        self.db.get_collection(self.obter_nome_collection()).update_one(query, update)

    def delete_many(self, query):
        self.db.get_collection(self.obter_nome_collection()).delete_many(query)

    def delete_one(self, query):
        self.db.get_collection(self.obter_nome_collection()).delete_one(query)

    def aggregation(self, aggregation):
        return self.db.get_collection(self.obter_nome_collection()).aggregate(aggregation)

    def criar_collection(self, nome_collection: str):
        with open(f'./assets/validator/{nome_collection}_validator.json') as collection_validator_file:
            collection_validator = json.load(collection_validator_file)

        try:
            self.db.create_collection(nome_collection)
        except Exception as e:
            print(e)

        self.db.command("collMod", nome_collection, validator=collection_validator)
