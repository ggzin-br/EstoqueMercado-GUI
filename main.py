# Trabalho CRUD - LTP2 - Fábio

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

import user
import produto

def main():

    ## Inicialização dos componentes do sistema
    user_db = user.DB_user("a.db")
    produto_db = produto.DB_produto("a.db")

    usuario: user.User

    def verificar_login():
        email = entry_email.get().strip()
        senha = entry_senha.get()

        global usuario 
        usuario = user.User(email, user_db.fazer_login(email, senha))

        if usuario.tok_auth:
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario.email}!")
            janela_login.destroy()
            abrir_janela_estoque()
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos.")

    def cadastrar_usuario():
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha e-mail e senha.")
            return

        try:
            user_db.inserir_usuario(email, senha)
            messagebox.showinfo("Cadastro", f"Usuário '{email}' cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "E-mail já cadastrado.")

    # --- Funções de Estoque ---
    def adicionar_produto():
        try:
            nome = entry_nome.get().strip()
            preco = float(entry_preco.get())
            quantidade = int(entry_quantidade.get())
            global usuario

            prod = produto.Produto(nome, preco)

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if produto_db.listar_produtos(usuario, prod):
                raise ValueError("Produto já cadastrado.")

            try:
                if user_db.is_user_logado(usuario):
                    produto_db.inserir_produto(prod, quantidade, usuario)
                    messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado ao estoque.")
                else:
                    messagebox.showinfo("Usuário não logado!")
                
                limpar_campos()
                atualizar_tabela()

            except sqlite3.IntegrityError as e:
                messagebox.showerror("Erro no DB", str(e))

        except ValueError as e:
            messagebox.showerror("Erro de valor", str(e))

    def excluir_produto():
        global usuario

        try:
            item_selecionado = tree.selection()
            if not item_selecionado:
                raise ValueError("Nenhum produto selecionado para exclusão.")
            nome = tree.item(item_selecionado)["values"][0]
            
            produto_db.excluir_item(nome)
            messagebox.showinfo("Sucesso", f"Produto '{nome}' excluído.")
            atualizar_tabela()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    def atualizar_tabela():
        global usuario

        for item in tree.get_children():
            tree.delete(item)

        if user_db.is_user_logado(usuario):
            for nome, quantidade in produto_db.listar_produtos(usuario):
                if nome != None:
                    tree.insert("", tk.END, values=(nome, str(quantidade)))

    def abrir_janela_estoque():
        global entry_nome, entry_preco, entry_quantidade, tree

        janela = tk.Tk()
        janela.title("Estoque de Mercado")
        janela.geometry("500x450")

        tk.Label(janela, text="Nome do Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_nome = tk.Entry(janela)
        entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(janela, text="Preço (R$):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_preco = tk.Entry(janela)
        entry_preco.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(janela, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_quantidade = tk.Entry(janela)
        entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(janela, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(janela, text="Excluir Produto", command=excluir_produto).grid(row=4, column=0, columnspan=2, pady=5)

        tree = ttk.Treeview(janela, columns=("Nome", "Quantidade"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("Quantidade", text="Quantidade")
        tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        atualizar_tabela()
        janela.mainloop()

    # --- Janela de Login ---
    janela_login = tk.Tk()
    janela_login.title("Login do Sistema")
    janela_login.geometry("300x230")

    tk.Label(janela_login, text="E-mail:").pack(pady=5)
    entry_email = tk.Entry(janela_login)
    entry_email.pack()

    tk.Label(janela_login, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(janela_login, show="*")
    entry_senha.pack()

    tk.Button(janela_login, text="Entrar", command=verificar_login).pack(pady=10)
    tk.Button(janela_login, text="Cadastrar Novo Usuário", command=cadastrar_usuario).pack()

    janela_login.mainloop()


if __name__ == "__main__":
    main()