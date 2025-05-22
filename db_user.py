import sqlite3
# Este arquivo será responsável por gerenciar o DB nas funções de criação de usuário e deleção

class DB_user:
    ## Atributos
    conexao: sqlite3.Connection
    cursor: sqlite3.Cursor
    __id_login: int = None

    ## Construtor
    def __init__(self, nome_db: str):
        self.conexao = sqlite3.connect(nome_db)
        self.cursor = self.conexao.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT DEFAULT NULL
            )
        """)

    # Fechar conexão
    def close_db(self):
        self.conexao.close()
    
    # Método de login
    def fazer_login(self, email:str, senha:str) -> tuple[int,] | None:
        self.cursor.execute("SELECT id FROM usuario WHERE email = ? AND senha = ?", (email, senha))
        return self.cursor.fetchone()

    # CREATE - Inserir usuário
    def inserir_usuario(self, email:str, senha:str) -> None:
        try:
            self.cursor.execute("INSERT INTO usuario (email, senha) VALUES(?,?)", (email, senha))
            self.conexao.commit()
            print(f"Usuário: \"{email}\" criado com sucesso!")
        except sqlite3.IntegrityError as e:
            print(f"Usuário \"{email}\" já existe: {e}")

    # READ - Listar ou ler usuários 
    def listar_users(self) -> list[str]:
        users: list[str]

        self.cursor.execute("SELECT id, email FROM usuario")
        users = self.cursor.fetchall()
        return users

    #DELETE - Excluir usuário
    def excluir_usuario(self, id:int) -> None:
        self.cursor.execute("DELETE FROM usuario WHERE id = ?", (id,))
        self.conexao.commit()

        if self.cursor.rowcount > 0:
            print(f"Usuário excluido com sucesso!")
        else:
            print("Usuário inexistente!")

# .commit() precisa ser usado em INSERT, UPDATE e DELETE
