## user.py
# Este módulo será usado para definir a estrutura do usuário e definir métodos para salva-lo e acessa-lo

import random
import sqlite3
from db import DB

class User:
    __email:str
    __tok_auth:int

    def __init__(self, email:str, tok_auth:int):
        self.__email = email
        self.__tok_auth = tok_auth

    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def tok_auth(self) -> int:
        return self.__tok_auth

class DB_user(DB):

    def __init__(self, nome_db: str):
        super().__init__(nome_db, """
        CREATE TABLE usuario (
            email    VARCHAR2(4000) NOT NULL,
            senha    VARCHAR2(4000) NOT NULL,
            tok_auth INTEGER NOT NULL,
            CONSTRAINT usuario_pk PRIMARY KEY (tok_auth)
        );

        ALTER TABLE usuario ADD CONSTRAINT usuario_pk PRIMARY KEY ( tok_auth );
        """)
    
    def fazer_login(self, email:str, senha:str) -> tuple[int] | None:
        self.cursor.execute("SELECT tok_auth FROM usuario WHERE email = ? AND senha = ?", (email, senha))
        tok_auth = self.cursor.fetchone()

        if tok_auth:
            return tok_auth[0]
        return None
    
    def is_user_logado(self, user:User) -> bool:
        self.cursor.execute("SELECT email FROM usuario WHERE tok_auth = ?", (user.tok_auth,))
        return bool(self.cursor.fetchone())

    def inserir_usuario(self, email:str, senha:str) -> int:

        ## Verificar se já existe um usuário contendo o mesmo número tok_auth
        VAL_MIN_TOK = 1
        VAL_MAX_TOK = 999999999999
        tok_auth:int = random.randint(VAL_MIN_TOK, VAL_MAX_TOK)
        self.cursor.execute("SELECT tok_auth FROM usuario")
        tok_em_uso:list[int] = self.cursor.fetchall()

        while tok_auth in tok_em_uso:
            tok_auth = random.randint(VAL_MIN_TOK, VAL_MAX_TOK)

        self.cursor.execute("INSERT INTO usuario (email, senha, tok_auth) VALUES(?,?,?)", (email, senha, tok_auth))
        self.conexao.commit()

        return tok_auth

    def listar_users(self) -> list[str]:
        users: list[str]

        self.cursor.execute("SELECT email FROM usuario")
        users = self.cursor.fetchall()
        return users

    def excluir_usuario(self, tok_auth:int) -> None:
        self.cursor.execute("DELETE FROM usuario WHERE tok_auth = ?", (email,))
        self.conexao.commit()

        if self.cursor.rowcount > 0:
            print(f"Usuário excluido com sucesso!")
        else:
            print("Usuário inexistente!")

# .commit() precisa ser usado em INSERT, UPDATE e DELETE
