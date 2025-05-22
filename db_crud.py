import sqlite3
# Este arquivo será responsável por gerenciar o DB nas funções básicas de CRUD

class DB_crud:
    ## Atributos
    conexao: sqlite3.Connection
    cursor: sqlite3.Cursor
    id_user: int

    ## Construtor
    def __init__(self, nome_db: str, id_user:int):
        self.conexao = sqlite3.connect(nome_db)
        self.cursor = self.conexao.cursor()
        self.id_user = id_user

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            qtd INTEGER NOT NULL,
            preco FLOAT NOT NULL,
            id_user INTEGER UNIQUE
            )
        """)
    

    # Fechar conexão
    def close_db(self):
        self.conexao.close()

    # CREATE - Inserir item
    def inserir_produto(self, nome:str, qtd:int, preco:float) -> None:
        try:
            self.cursor.execute("INSERT INTO produto (nome,qtd,preco,id_user) VALUES(?,?,?,?)", 
                        (nome,qtd,preco,self.id_user))
            self.conexao.commit()
            print(f"Produto \"{nome}\" inserido com sucesso")
        except sqlite3.IntegrityError:
            print("Erro: Produto já existente")


    # READ - Listar ou ler produtos 
    def listar_produtos(self) -> list[str]:
        produtos: list[str]

        self.cursor.execute("SELECT * FROM produto WHERE id_user = ?", (self.id_user,))
        produtos = self.cursor.fetchall()
        return produtos


    #UPDATE - Atualizar instancia(linha) do item
    def atualizar_item(self, id:int, nome:str, qtd:int, preco:float):
        self.cursor.execute("UPDATE produto SET nome = ?, qtd = ?, preco = ? WHERE id = ? AND id_user = ?",
        (nome, qtd, preco, id, self.id_user))
        self.conexao.commit()
        
        if self.cursor.rowcount > 0:
            print("Produto atualizado com sucesso!")
        else:
            print("Produto não encontrado!")


    #DELETE - Excluir produto
    def excluir_item(self, id) -> None:
        self.cursor.execute("DELETE FROM produto WHERE id = ? AND id_user = ?", (id,self.id_user))
        self.conexao.commit()

        if self.cursor.rowcount > 0:
            print("Produto excluido com sucesso!")
        else:
            print("Produto não encontrado!")
