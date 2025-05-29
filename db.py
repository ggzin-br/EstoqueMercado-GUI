import sqlite3

class DB:
    __conexao:sqlite3.Connection
    __cursor:sqlite3.Cursor

    def __init__(self, nome_db:str, create_db_query:str):
        self.__conexao = sqlite3.connect(nome_db)
        self.__cursor = self.__conexao.cursor()

        try:
            self.__cursor.executescript(create_db_query)
        except sqlite3.OperationalError:
            print(f"{nome_db} já existe!, seguindo com o existente...")
        except sqlite3.Error as e:
            print(f"Erro: ", e)

    def close_db(self):
        self.__conexao.close()

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor
    
    @property
    def conexao(self) -> sqlite3.Connection:
        return self.__conexao