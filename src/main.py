from databases.msql_connect import MySQlConnect
from databases.mongodb_connect import MongoDBConnect
from config.database_config import get_database_config
from databases.schema_manager import create_mysql_schema


def main(config):
    # mysql
    config_mysql = config["mysql"]
    with MySQlConnect(config_mysql.host, config_mysql.port, config_mysql.user, config_mysql.password) as mysql_client:
        connection, cursor = mysql_client.connection, mysql_client.cursor
        create_mysql_schema(connection,cursor)

    #mongodb
    # config_mongodb = config["mongodb"]
    # with MongoDBConnect(config_mongodb.uri, config_mongodb.database) as mongo_client:
    #     mongo_client.connect()

if __name__ == "__main__":
    config = get_database_config()
    main(config)