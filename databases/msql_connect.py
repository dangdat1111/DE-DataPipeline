
import mysql.connector
from mysql.connector import Error
# Mysql connector
class MySQlConnect:
    #Hàm init: Một hàm khởi tạo (constructor) → Khi gọi class MySQLConnect thì hàm init sẽ khởi tạo/sẽ chạy trước tiên. Trong hàm này chứa các giá trị bắt buộc phải truyền vào
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.config = {
        'host': host,
        'port' : port,
        'user': user,
        'password' : password
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            print('--------------Connected to MYSQL---------------')
            return self.connection, self.cursor
        except Error as e:
            raise Exception(f'------------Fail to connect Mysql: {e}') from e

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('------------------MYSQL Close Connection--------------')

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()




