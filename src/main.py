from databases.msql_connect import MySQlConnect
from config.database_config import get_database_config
def main(config):
    with MySQlConnect(config["mysql"].host, config["mysql"].port, config["mysql"].user, config["mysql"].password) as mysql_client:
        mysql_client.connect()


if __name__ == "__main__":
    config = get_database_config()
    main(config)