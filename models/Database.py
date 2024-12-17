import mariadb
import Database.querys as db
import os
from dotenv import load_dotenv

class Database:
    _instance = None  # Atributo de classe para armazenar a única instância

    def __new__(cls, *args, **kwargs):
        """Garante que apenas uma instância da classe seja criada."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False  # Flag para inicialização
        return cls._instance

    def __init__(self):
        """Evita reinicializar a instância existente."""
        if self._initialized:
            return
        
        load_dotenv()  # Carrega as variáveis do arquivo .env
        self._hostname: str = os.getenv("DB_HOST")  
        self._user: str = os.getenv("DB_USER")  
        self._password: str = os.getenv("DB_PASSWORD")  
        self._db_name: str = os.getenv("DB_NAME")  
        self._port: int = int(os.getenv("DB_PORT", 3306))
        self._connect()
        self._initialized = True

    def _connect(self):
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.db = mariadb.connect(
                host=self._hostname,
                port=3306,
                user=self._user,
                password=self._password,
                database=self._db_name
            )
            print("Conexão bem-sucedida com o banco MariaDB!")
        except mariadb.Error as e:
            print(f"Erro ao conectar ao MariaDB: {e}")
            self.db = None

    def _check_connection(self):
        """Verifica se a conexão ainda está ativa, reconectando se necessário."""
        try:
            self.db.ping()  # Verifica se a conexão está ativa
        except mariadb.Error:
            print("Conexão perdida. Reconectando...")
            self._connect()

    def execute_query(self, query: str, values: tuple = None) -> bool:
        self._check_connection()
        try:
            mycursor = self.db.cursor()
            if values:
                mycursor.execute(query, values)
            else:
                mycursor.execute(query)
            self.db.commit()
            return True
        except mariadb.Error as e:
            print(f"Erro ao executar query: {e}")
            return False
        finally:
            mycursor.close()

    def execute_select_query(self, query: str, values: tuple = None) -> list:
        self._check_connection()
        try:
            mycursor = self.db.cursor()
            if values:
                mycursor.execute(query, values)
            else:
                mycursor.execute(query)
            return mycursor.fetchall()
        except mariadb.Error as e:
            print(f"Erro ao executar SELECT query: {e}")
            return []
        finally:
            mycursor.close()

    def return_last_insert(self):
        try:
            mycursor = self.db.cursor()
            mycursor.execute("SELECT LAST_INSERT_ID()")
            id = mycursor.fetchone()[0]
            return id
        finally:
            mycursor.close()
    
    