## estoque.py
# É responsável por gerenciar o estoque relacionado com um usuário

import sqlite3
from db import DB
from user import User
from user import DB_user

class Produto:
    __nome:str
    __preco:str

    def __init__(self, nome:str, preco:str):
        self.__nome = nome
        self.__preco = preco

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def preco(self) -> str:
        return self.__preco
    @preco.setter
    def preco(self, preco:float) -> None:
        self.__preco = preco

class DB_produto(DB):

    def __init__(self, nome_db: str):
        
        super().__init__(nome_db, """
        CREATE TABLE produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,                  
            preco REAL NOT NULL,                 
            usuario_tok_auth INTEGER,            

            FOREIGN KEY (usuario_tok_auth) REFERENCES usuario (tok_auth)
        );
        """)

    def inserir_produto(self, produto:Produto, qtd:int, user:User) -> None:
        for _ in range(qtd):
            self.cursor.execute("INSERT INTO produto (nome,preco,usuario_tok_auth) VALUES(?,?,?)", (produto.nome, produto.preco, user.tok_auth))
            self.conexao.commit()
            print(f"Produto \"{produto.nome}\" inserido com sucesso")


    # READ - Listar ou ler produtos 
    def listar_produtos(self, user: User, produto: Produto=None) -> list[str] | None:
        produtos: list[str]

        self.cursor.execute("""
        SELECT 
            p.nome,
            COUNT(*)
        FROM produto AS p
        LEFT JOIN usuario AS u ON p.usuario_tok_auth = u.tok_auth
        WHERE p.usuario_tok_auth = ?
        """,(user.tok_auth,))
        produtos = self.cursor.fetchall()
        print(produtos)
        return produtos


    #UPDATE - Atualizar instancia(linha) do item
    def atualizar_item(self, id:int, nome:str, qtd:int, preco:float):
        self.cursor.execute("",)
        self.conexao.commit()
        
        if self.__db.cursor.rowcount > 0:
            print("Produto atualizado com sucesso!")
        else:
            print("Produto não encontrado!")


    #DELETE - Excluir produto
    def excluir_item(self, nome) -> None:
        self.cursor.execute("DELETE FROM produto WHERE nome = ?",(nome,))
        self.conexao.commit()

        if self.cursor.rowcount > 0:
            print("Produto excluido com sucesso!")
        else:
            print("Produto não encontrado!")
