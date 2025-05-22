## estoque.py
# É responsável por gerenciar o estoque relacionado com um usuário

import sqlite3
from db import DB
from produto_temp import Produto

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
        
        super(nome_db, """
        CREATE TABLE produto (
            nome             VARCHAR2(4000) NOT NULL,
            preco            NUMBER NOT NULL,
            id               INTEGER NOT NULL AUTO INCREMENT,
            usuario_tok_auth INTEGER
        );

        ALTER TABLE produto ADD CONSTRAINT produto_pk PRIMARY KEY ( id );
              
        ALTER TABLE produto
            ADD CONSTRAINT produto_usuario_fk FOREIGN KEY ( usuario_tok_auth )
                REFERENCES usuario ( tok_auth );
        """)

    def inserir_produto(self, produto: Produto, qtd:int) -> None:
        try:
            for _ in qtd:
                self.cursor.execute("INSERT INTO produto (nome,preco) VALUES(?,?)", (produto.nome, produto.preco))
                self.conexao.commit()
                print(f"Produto \"{produto.nome}\" inserido com sucesso")
        except sqlite3.IntegrityError:
            print("Erro: ID já existente")


    # READ - Listar ou ler produtos 
    def listar_produtos(self) -> list[str]:
        produtos: list[str]

        self.conexao.execute("",)
        produtos = self.cursor.fetchall()
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
    def excluir_item(self, id) -> None:
        self.cursor.execute("",)
        self.conexao.commit()

        if self.cursor.rowcount > 0:
            print("Produto excluido com sucesso!")
        else:
            print("Produto não encontrado!")
