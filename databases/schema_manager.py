# dùng python tạo database-schema với mysql, mongodb
from mysql.connector import Error

def create_mysql_schema(connection, cursor):
    # truyền vào kết nối với mysql
    # tạo database "github_database"
    database = "github_data"
    cursor.execute(f"DROP DATABASE IF EXISTS {database}")
    print(f"---------_DROP database : {database} in MYSQL---------")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    print(f"---------_CREATE database : {database} in MYSQL---------")

    connection.database = database
    connection.commit()

    try:
        with open('/home/prime/dangdat1111/DE-DataPipeline/src/sql/schema.sql', 'r') as f:
            sql_script = f.read()
            # print(sql_script)
            # cursor.execute(f"USE {database}")
            cursor.execute(sql_script)
            connection.commit()
            print("----------_CREATED MYSQL SCHEMA-------------")
    except Error as e:
        connection.rollback()
        raise Exception(f"-----------Failed to CREATE MYSQL SCHEMA. ERROR : {e}") from e

# def create_mongodb_schema()


