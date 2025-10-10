# Mục đích: lấy thông tin của database ( mysql, mongodb ) từ file .env
from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class MySQLConfig():
    host : str
    user : str
    password : str
    database : str
    port : int

def get_database_config():
    # load config first
    load_dotenv()

    config = {
        "mysql": MySQLConfig(
            host = os.getenv("MYSQL_HOST"),
            port = os.getenv("MYSQL_PORT"),
            user = os.getenv("MYSQL_USER"),
            password = os.getenv("MYSQL_PASSWORD"),
            database = os.getenv("MYSQL_DATABASE")
        ),
    }

    return config


config =  get_database_config()
print(config)