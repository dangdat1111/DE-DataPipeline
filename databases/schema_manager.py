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
    db.create_collection("users", validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "login"],  # _id sẽ là user_id
            "properties": {
                "_id": {"bsonType": "int", "description": "user_id từ GitHub"},
                "login": {
                    "bsonType": "string",

                },
                "avatar_url": {"bsonType": ["string", "null"]},
                "url": {"bsonType": ["string", "null"]},
                "type": {"bsonType": "string", "enum": ["User", "Organization"]},
                "site_admin": {"bsonType": "bool"},
                "created_at": {"bsonType": "date"}
            }
        }
    })

    db.drop_collection("orgs")
    db.create_collection("orgs", validator ={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "login"],  # _id sẽ là org_id
            "properties": {
                "_id": {"bsonType": "long", "description": "org_id từ GitHub"},
                "login": {"bsonType": "string"},
                "url": {"bsonType": "string"},
                "avatar_url": {"bsonType": "string"},
                "created_at": {"bsonType": "date"}
            }
        }
    })

    db.drop_collection("repos")
    db.create_collection("repos", validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name", "full_name", "owner"],
            "properties": {
                "_id": {"bsonType": "long", "description": "repo_id từ GitHub"},
                "name": {"bsonType": "string"},
                "full_name": {"bsonType": "string"},
                "url": {"bsonType": "string"},
                "html_url": {"bsonType": "string"},
                "description": {"bsonType": ["string", "null"]},  # Có thể null
                "is_private": {"bsonType": "bool"},
                "is_fork": {"bsonType": "bool"},
                "stats": {  # Gom nhóm các chỉ số thống kê cho gọn
                    "bsonType": "object",
                    "properties": {
                        "size": {"bsonType": "int"},
                        "forks_count": {"bsonType": "int"},
                        "stargazers_count": {"bsonType": "int"},
                        "watchers_count": {"bsonType": "int"}
                    }
                },
                "language": {"bsonType": ["string", "null"]},
                "default_branch": {"bsonType": "string"},
                "dates": {  # Gom nhóm ngày tháng
                    "bsonType": "object",
                    "properties": {
                        "created_at": {"bsonType": "date"},
                        "updated_at": {"bsonType": "date"},
                        "pushed_at": {"bsonType": "date"}
                    }
                },
                # --- NHÚNG (Embedding) thay thế cho bảng REPO_OWNERSHIP ---
                "owner": {
                    "bsonType": "object",
                    "required": ["id", "login", "type"],
                    "properties": {
                        "id": {"bsonType": "long", "description": "user_id hoặc org_id"},
                        "login": {"bsonType": "string"},
                        "type": {"bsonType": "string", "enum": ["User", "Organization"]}
                    }
                }
            }
        }
    })

    db.drop_collection("events")
    db.create_collection("events", validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "type", "actor", "repo", "created_at"],
            "properties": {
                "_id": {"bsonType": "string", "description": "event_id"},
                "type": {"bsonType": "string"},  # ForkEvent, PushEvent, v.v.
                "is_public": {"bsonType": "bool"},
                "created_at": {"bsonType": "date"},

                # Actor: Nhúng một phần thông tin User
                "actor": {
                    "bsonType": "object",
                    "required": ["id", "login"],
                    "properties": {
                        "id": {"bsonType": "long"},
                        "login": {"bsonType": "string"},
                        "avatar_url": {"bsonType": "string"}
                    }
                },

                # Repo: Nhúng một phần thông tin Repo gốc
                "repo": {
                    "bsonType": "object",
                    "required": ["id", "name", "url"],
                    "properties": {
                        "id": {"bsonType": "long"},
                        "name": {"bsonType": "string"},  # format: owner/repo
                        "url": {"bsonType": "string"}
                    }
                },

                # Org: (Optional)
                "org": {
                    "bsonType": ["object", "null"],
                    "properties": {
                        "id": {"bsonType": "long"},
                        "login": {"bsonType": "string"}
                    }
                },

                # PAYLOAD: Chứa thông tin linh động tùy loại event (Thay thế cột forkee_repo_id)
                "payload": {
                    "bsonType": "object",
                    "properties": {
                        # Nếu là ForkEvent, thông tin forkee sẽ nằm ở đây
                        "forkee": {
                            "bsonType": "object",
                            "properties": {
                                "id": {"bsonType": "long"},
                                "name": {"bsonType": "string"},
                                "public": {"bsonType": "bool"}
                            }
                        },
                        # Các field khác cho PushEvent, PullRequestEvent... sẽ nằm ở đây
                        "ref": {"bsonType": "string"},
                        "head": {"bsonType": "string"}
                    }
                }
            }
        }
    })

    db.users.create_index("login", unique=True)

    # Index cho Repos
    db.repos.create_index("full_name", unique=True)
    db.repos.create_index("owner.id")  # Tìm repo theo owner nhanh hơn

    # Index cho Events
    db.events.create_index("actor.id")  # Tìm event của 1 người
    db.events.create_index("repo.id")  # Tìm event của 1 repo
    print("----------_CREATED MONGODB SCHEMA-------------")









