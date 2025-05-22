# Trabalho CRUD - LTP2 - Fábio

import tkinter as tk
from tkinter import messagebox

def main(): 
    

    def executar_acao(acao):
        messagebox.showinfo("Ação", f"Você clicou em: {acao}")

    root = tk.Tk()
    root.title("Menu Colorido com Tkinter Puro")
    root.geometry("900x600")
    root.resizable(False, False)

    # Frame principal com cor
    frame_principal = tk.Frame(root, bg="#65dda2", padx=20, pady=20)
    frame_principal.pack(expand=True, fill='both')

    # Subframe colorido para o menu
    frame_menu = tk.Frame(frame_principal, bg="#d0e0f0", padx=10, pady=10, bd=2, relief="groove")
    frame_menu.pack(pady=20)

    # Botões individuais com cores
    btn_novo = tk.Button(frame_menu, text="Novo", bg="#4caf50", fg="white", width=15, height=2,
                        command=lambda: executar_acao("Novo"))
    btn_novo.grid(row=0, column=0, padx=20, pady=20)

    btn_abrir = tk.Button(frame_menu, text="Abrir", bg="#2196f3", fg="white", width=15, height=2,
                        command=lambda: executar_acao("Abrir"))
    btn_abrir.grid(row=0, column=1, padx=20, pady=20)

    btn_salvar = tk.Button(frame_menu, text="Salvar", bg="#ff9800", fg="white", width=15, height=2,
                        command=lambda: executar_acao("Salvar"))
    btn_salvar.grid(row=1, column=0, padx=20, pady=10)

    btn_exportar = tk.Button(frame_menu, text="Exportar", bg="#9c27b0", fg="white", width=15, height=2,
                            command=lambda: executar_acao("Exportar"))
    btn_exportar.grid(row=1, column=1, padx=20, pady=10)

    btn_fechar = tk.Button(frame_menu, text="Fechar", bg="#f44336", fg="white", width=32, height=2,
                       command=root.destroy)
    btn_fechar.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()