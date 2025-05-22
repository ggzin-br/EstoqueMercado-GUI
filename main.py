# Trabalho CRUD - LTP2 - Fábio
# Pedro Resende
# Pedro Garcia
import db_crud
import db_user
from simple_term_menu import TerminalMenu

# Declaracao de variaveis:
optionsMenu = []
optionsUser = []
oprionsCrud = []
menu_entry_index = ''
choice = ''

# Funcoes para abrir os menus:
# func para mostrar o menu principal
def show_menu_main():
    global optionsMenu
    optionsMenu = ["[1]Menu de Usuários","[2]Menu de Produtos","[3]Sair"]
    terminal_menu = TerminalMenu(optionsMenu,title="\nO que deseja fazer??\n")
    global menu_entry_index
    menu_entry_index = terminal_menu.show()


# func para mostrar o menu do crud/gerenciamento de produtos
def show_menu_crud():
    global optionsCrud 
    optionsCrud = ["[1]Listar produtos","[2]Adicionar produto","[3]Remover produto","[4]Atualizar produto","[5]Sair"]
    terminal_menu = TerminalMenu(optionsCrud,title="\nO que deseja fazer??\n")
    global menu_entry_index 
    menu_entry_index= terminal_menu.show()


# func para mostras o menu dos usuarios
def show_menu_user():
    global optionsUser
    optionsUser = ["[1]Listar usuários","[2]Adicionar usuário","[3]Remover usuário","[4]Login","[5]Sair"]
    terminal_menu = TerminalMenu(optionsUser,title="\nO que deseja fazer??\n")
    global menu_entry_index 
    menu_entry_index= terminal_menu.show()


# Funcoes para operacoes nos menus
# func para realizar operacoes no menu dos produtos
def menu_estoque_produto(id_user:int): 

    ## Declarações
    db:db_crud.DB_crud = db_crud.DB_crud("mercado_estoque.db", id_user)

    id:int
    nome:str
    qtd:int
    preco:float

    ## Algoritmo
    while True:
        show_menu_crud()
        global choice
        choice = optionsCrud[menu_entry_index]
        match choice:
            case "[1]Listar produtos":
               for i in db.listar_produtos():
                    print(f"Id: {i[0]}\n Nome: {i[1]}\n Qtd: {i[2]}\n Preço: {i[3]}")
                    print("\n")
                   
            case "[2]Adicionar produto":
                try:
                    nome = input("Digite o nome do produto: ").strip()
                    qtd = int(input("Digite a quantidade em estoque do produto: ").strip())
                    preco = float(input("Digite o preço do produto: ").strip())
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue
                
                db.inserir_produto(nome,qtd,preco)

            case "[3]Remover produto":
                try:
                    id = int(input("Digite o id do produto que deseja ser deletado: ").strip())
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue

                db.excluir_item(id)

            case "[4]Atualizar produto":
                try:
                    id = int(input("Digite o id do produto que deseja alterar: ").strip())
                    nome = input("Digite o novo nome do produto:  ").strip()
                    qtd = int(input("Digite a nova quantidade em estoque do produto: ").strip())
                    preco = float(input("Digite o  novo preço do produto: ").strip())
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue

                db.atualizar_item(id,nome,qtd,preco)

            case "[5]Sair":
                print("Saindo, volte sempre!")
                break

    db.close_db()

# func para realizar operacoes no menu dos usuarios
# Ele retorna no caso do login
def menu_users() -> int | None:

    ## Declarações
    db:db_user.DB_user = db_user.DB_user("usuarios.db")
    email: str
    senha: str
    id: int

    ## Algoritmo
    while True:
        show_menu_user()

        global choice
        choice = optionsUser[menu_entry_index]
        match choice:
            case "[1]Listar usuários":
                for i in db.listar_users():
                    print(f"Id: {i[0]}\n e-mail: {i[1]}")
                    print("\n")

            case "[2]Adicionar usuário":
                try:
                    email = input("Digite o email do usuário: ").strip()
                    senha = input("Digite a senha do usuário: ").strip()
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue

                db.inserir_usuario(email,senha)

            case "[3]Remover usuário":
                try:
                    id = int(input("Digite o id do produto que deseja ser deletado: ").strip())
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue
                
                db.excluir_usuario(id)

            case "[4]Login": 
                try:
                    email = input("Digite o email do usuário: ").strip()
                    senha = input("Digite a senha do usuário: ").strip()
                except ValueError as e:
                    print(f"Digite um valor válido: {e}")
                    continue
                
                return db.fazer_login(email, senha)

            case "[5]Sair":
                print("Saindo, volte sempre!")
                break
    
    db.close_db()


def main(): 

    id_user_logado:int | None = None

    while True:
        global choice
        show_menu_main()
        choice = optionsMenu[menu_entry_index]
        match choice:
            case "[1]Menu de Usuários":
                id_user_logado = menu_users()
            case "[2]Menu de Produtos":
                if id_user_logado == None:
                    print("Faça o login antes")
                    continue
                menu_estoque_produto(id_user_logado[0])
            case "[3]Sair":
                print("Saindo, volte sempre!")
                break

if __name__ == "__main__":
    main()