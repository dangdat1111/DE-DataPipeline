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
    connection.commit()
    connection.database = database


    try:
        with open('/home/prime/dangdat1111/DE-DataPipeline/src/sql/schema.sql', 'r') as f:
            sql_script = f.read()
            # thực thi từng câu lệnh trong file schema.sql
            sql_commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]
            for cmd in sql_commands:
                cursor.execute(cmd)
                print(f'--------------Executed Mysql Command: {cmd}-----------')

            # thực thi toàn bộ file schema.sql
            # cursor.execute(sql_script)
            connection.commit()
            print("----------_CREATED MYSQL SCHEMA-------------")
    except Error as e:
        connection.rollback()
        raise Exception(f"-----------Failed to CREATE MYSQL SCHEMA. ERROR : {e}") from e

def create_mongodb_schema(db):
    db.drop_collection("users")
    db.drop_collection("orgs")
    db.drop_collection("repos")
    db.drop_collection("events")




