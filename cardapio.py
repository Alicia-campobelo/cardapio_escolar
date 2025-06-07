import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import sqlite3

class Application:
    def __init__(self):
        self.tema()
        self.conectar_banco()
        self.criar_tabela_usuarios()
        self.tela()
        self.tela_login()
        self.janela.mainloop()
        
#Layout

    def tema(self):
        ctk.set_appearance_mode("Dark")
        
#Bancos

    def conectar_banco(self):
        self.conn = sqlite3.connect("sistema.db")
        self.cursor = self.conn.cursor()

    def criar_tabela_usuarios(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                calorias INTEGER NOT NULL
            )
        """)
        self.conn.commit()
        
#Telas-Login

    def tela(self):
        self.janela = ctk.CTk()
        self.janela.geometry("700x400")
        self.janela.title("Sistema de Login")
        self.janela.resizable(False, False)
        
#Tela de Login (Imagem, botões)

    def tela_login(self):
        imagem_original = Image.open("img/f.png")
        imagem_redimensionada = imagem_original.resize((250, 250))
        img = ImageTk.PhotoImage(imagem_redimensionada)
        
        pos_x = (350 - 200) // 2
        pos_y = (400 - 200) // 2
        
        label_img = ctk.CTkLabel(master=self.janela, image=img, text="")
        label_img.image = img
        label_img.place(x=pos_x, y=pos_y)
        
        label_tt = ctk.CTkLabel(master=self.janela, text="Cardápio", font=("Arial", 30), text_color="#ff0000")
        label_tt.place(x=125, y=60)

        login_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        login_frame.pack(side=ctk.RIGHT)

        ctk.CTkLabel(master=login_frame, text="Login", font=("Arial", 16)).place(x=25, y=5)

        self.username_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Nome de usuário", width=300)
        self.username_entry.place(x=25, y=50)

        self.password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Senha", width=260, show="*")
        self.password_entry.place(x=25, y=100)

        self.eye_open_img = ctk.CTkImage(Image.open("img/eye.png").resize((20, 20)))
        self.eye_closed_img = ctk.CTkImage(Image.open("img/eye_off.png").resize((20, 20)))

        self.mostrar_senha = False

        self.eye_button = ctk.CTkButton(master=login_frame, width=30, height=28, text="", image=self.eye_closed_img, command=self.toggle_senha)
        self.eye_button.place(x=290, y=100)

        ctk.CTkButton(master=login_frame, text="Login", command=self.autenticar, width=300).place(x=25, y=170)
        ctk.CTkLabel(master=login_frame, text="Se não tem uma conta", font=("Arial", 10)).place(x=25, y=220)

        ctk.CTkButton(master=login_frame, text="Cadastre-se", command=self.abrir_janela_cadastro, width=150, fg_color="green").place(x=160, y=220)
        ctk.CTkButton(master=login_frame, text="Editar Perfil", command=self.abrir_janela_editar, width=300, fg_color="#ffa500").place(x=25, y=270)
        ctk.CTkButton(master=login_frame, text="Excluir Perfil", command=self.excluir_perfil, width=300, fg_color="red").place(x=25, y=320)

    def toggle_senha(self):
        self.mostrar_senha = not self.mostrar_senha
        if self.mostrar_senha:
            self.password_entry.configure(show="")
            self.eye_button.configure(image=self.eye_open_img)
        else:
            self.password_entry.configure(show="*")
            self.eye_button.configure(image=self.eye_closed_img)

    def autenticar(self):
        usuario = self.username_entry.get()
        senha = self.password_entry.get()

        self.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
        resultado = self.cursor.fetchone()

        if resultado:
            self.usuario_logado = resultado[1]
            self.abrir_janela_principal()
        else:
            messagebox.showerror("Erro de login", "Nome de usuário ou senha incorretos.")

    def abrir_janela_cadastro(self):
        janela = ctk.CTkToplevel(self.janela)
        janela.geometry("400x300")
        janela.title("Cadastro de novo usuário")
        
        janela.resizable(False, False)

        ctk.CTkLabel(janela, text="Cadastro", font=("Arial", 20)).pack(pady=10)
       
        janela.transient(self.janela)
        janela.grab_set()
        janela.focus()
        
        nome_entry = ctk.CTkEntry(janela, placeholder_text="Nome de usuário", width=300)
        nome_entry.pack(pady=10)

        senha_entry = ctk.CTkEntry(janela, placeholder_text="Senha", show="*", width=300)
        senha_entry.pack(pady=10)

        def cadastrar():
            nome = nome_entry.get()
            senha = senha_entry.get()

            if not nome or not senha:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            try:
                self.cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado!")
                janela.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Nome de usuário já existe.")

        ctk.CTkButton(janela, text="Cadastrar", command=cadastrar).pack(pady=10)
    
    def abrir_janela_principal(self):
       nova_janela = tk.Toplevel(self.janela)
       nova_janela.geometry("600x500")
       nova_janela.title(f"Bem-vindo(a), {self.usuario_logado}")
       nova_janela.resizable(False, False)

       label = tk.Label(nova_janela, text=f"Olá, {self.usuario_logado}!", font=("Arial", 18))
       label.pack(pady=10)

       btn_cardapio = tk.Button(nova_janela, text="Abrir Cardápio",font=("Arial", 14,"bold"), fg="blue", width=25, height=2, command=self.abrir_cardapio)
       btn_cardapio.pack(pady=20)
       
       btn_relatorios = tk.Button(nova_janela, text="Abrir Relatórios", font=("Arial", 14,"bold"), fg="purple", width=25, height=2, command=self.abrir_relatorios)
       btn_relatorios.pack(pady=40)

       btn_voltar = tk.Button(nova_janela, text="Voltar para a tela de Login", font=("Arial", 14,"bold"), fg="red", width=25, height=2, command=lambda: self.voltar_para_login(nova_janela))
       btn_voltar.pack(pady=15)
       
    def abrir_relatorios(self):
       janela_relatorios = tk.Toplevel(self.janela)
       janela_relatorios.title("Relatórios")
       janela_relatorios.geometry("600x400")
       janela_relatorios.resizable(False, False)
       
       ttk.Label(janela_relatorios, text="Selecione o Dia da Semana:", 
                font=("Arial", 12, "bold")).pack(pady=10)
       
       dias_da_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
       dia_selecionado = tk.StringVar()
       combobox_dias = ttk.Combobox(janela_relatorios, width=30, textvariable=dia_selecionado)
       combobox_dias['values'] = dias_da_semana
       combobox_dias.current(0)
       combobox_dias.pack(pady=10)
       
       frame_refeicoes = tk.Frame(janela_relatorios)
       frame_refeicoes.pack(pady=20)

       label_cafe = tk.Label(frame_refeicoes, text="Café da Manhã: Pão com manteiga e café", font=("Arial", 10))
       label_cafe.pack(anchor='w')

       label_almoco = tk.Label(frame_refeicoes, text="Almoço: Arroz, feijão, frango grelhado e salada", font=("Arial", 10))
       label_almoco.pack(anchor='w')

       label_janta = tk.Label(frame_refeicoes, text="Jantar: Sopa de legumes com torradas", font=("Arial", 10))
       label_janta.pack(anchor='w')
       
       def atualizar_refeicoes(event):
        dia = dia_selecionado.get()
        label_cafe.config(text=f"Café da Manhã ({dia}): Pão com manteiga e café")
        label_almoco.config(text=f"Almoço ({dia}): Arroz, feijão, frango grelhado e salada")
        label_janta.config(text=f"Jantar ({dia}): Sopa de legumes com torradas")

       combobox_dias.bind("<<ComboboxSelected>>", atualizar_refeicoes)
       
       frame_botoes = tk.Frame(janela_relatorios)
       frame_botoes.pack(pady=20)

       btn_adicionar = tk.Button(frame_botoes, text="Adicionar", font=("Arial", 10, "bold"), width=12, command=lambda: print("Adicionar refeição"))
       btn_adicionar.grid(row=0, column=0, padx=5, pady=5)

       btn_editar = tk.Button(frame_botoes, text="Editar", font=("Arial", 10, "bold"), width=12, command=lambda: print("Editar refeição"))
       btn_editar.grid(row=0, column=1, padx=5, pady=5)

       btn_excluir = tk.Button(frame_botoes, text="Excluir", font=("Arial", 10, "bold"), width=12, command=lambda: print("Excluir refeição"))
       btn_excluir.grid(row=0, column=2, padx=5, pady=5)

       btn_voltar = tk.Button(janela_relatorios, text="Voltar", font=("Arial", 10, "bold"), fg="red", width=15, command=janela_relatorios.destroy)
       btn_voltar.pack(pady=10)

    def voltar_para_login(self, janela_atual):
       janela_atual.destroy()  
       self.janela.deiconify()
    
    def abrir_janela_editar(self):
        nome = self.username_entry.get()
        senha = self.password_entry.get()

        self.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
        usuario = self.cursor.fetchone()

        if not usuario:
            messagebox.showerror("Erro", "Você precisa inserir nome e senha válidos antes de editar o perfil.")
            return

        janela = ctk.CTkToplevel(self.janela)
        janela.geometry("400x250")
        janela.title("Editar Perfil")

        ctk.CTkLabel(janela, text="Editar Usuário", font=("Arial", 20)).pack(pady=10)

        novo_nome = ctk.CTkEntry(janela, placeholder_text="Novo nome de usuário", width=300)
        novo_nome.pack(pady=5)

        nova_senha = ctk.CTkEntry(janela, placeholder_text="Nova senha", show="*", width=300)
        nova_senha.pack(pady=5)

        def salvar_edicao():
            janela = ctk.CTkToplevel(self.janela)
            janela.geometry("400x300")
            janela.title("Editar Perfil")
            novo = novo_nome.get()
            nova = nova_senha.get()
            
            janela.resizable(False, False)
            janela.transient(self.janela)
            janela.grab_set()
            janela.focus()

            if not novo or not nova:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            try:
                self.cursor.execute("UPDATE usuarios SET nome=?, senha=? WHERE nome=?", (novo, nova, nome))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Perfil atualizado.")
                janela.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Nome de usuário já existe.")

        ctk.CTkButton(janela, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)

    def excluir_perfil(self):
        nome = self.username_entry.get()
        senha = self.password_entry.get()

        self.cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
        usuario = self.cursor.fetchone()

        if not usuario:
            messagebox.showerror("Erro", "Você precisa inserir nome e senha válidos para excluir o perfil.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir seu perfil? Essa ação não poderá ser desfeita.")
        if confirmacao:
            self.cursor.execute("DELETE FROM usuarios WHERE nome=?", (nome,))
            self.conn.commit()
            messagebox.showinfo("Removido", "Seu perfil foi deletado.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def abrir_cardapio(self):
        janela_cardapio = tk.Toplevel()
        janela_cardapio.geometry("600x400")
        janela_cardapio.title("Lista de Alimentos")
        janela_cardapio.resizable(False, False)

        tree = ttk.Treeview(
            janela_cardapio, 
            columns=("ID", "Alimento", "Calorias", "Quantidade", "Validade"), 
            show="headings", 
            height=15 
        )

        tree.heading("ID", text="ID")
        tree.heading("Alimento", text="Alimento")
        tree.heading("Calorias", text="Calorias")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Validade", text="Validade")

        tree.column("ID", width=50, anchor="center")
        tree.column("Alimento", width=150, anchor="center")
        tree.column("Calorias", width=80, anchor="center")
        tree.column("Quantidade", width=100, anchor="center")
        tree.column("Validade", width=100, anchor="center")
        
        dados = [
        (1, "Batata", 8000, "10kg", "01/01/2050"),
        (2, "Cenoura", 2050, "5kg", "12/12/2025"),
        (3, "Beterraba", 450, "3kg", "10/10/2030"),
        (4, "Arroz", 65000, "50kg", "31/12/2099"),
        (5, "Feijão", 1685000, "50kg", "22/02/2077")
    ]

        for item in dados:
         tree.insert("", tk.END, values=item)

        self.cursor.execute("SELECT * FROM alimentos")
        for row in self.cursor.fetchall():
            tree.insert("", tk.END, values=row)
            
        tree.place(x=10, y=10, width=580, height=350)
    
        def adicionar_item():
            janela_adicionar = tk.Toplevel()
            janela_adicionar.title("Adicionar Item")
            janela_adicionar.geometry("300x250")
            janela_adicionar.resizable(False, False)

            labels = ["Alimento", "Calorias", "Quantidade", "Validade"]
            entradas = []

            for label in labels:
                tk.Label(janela_adicionar, text=label).pack()
                entrada = tk.Entry(janela_adicionar)
                entrada.pack()
                entradas.append(entrada)

            def salvar_novo():
                novo_id = len(tree.get_children()) + 1
                novo_item = (
                    novo_id,
                    entradas[0].get(),
                    entradas[1].get(),
                    entradas[2].get(),
                    entradas[3].get()
                )
                tree.insert("", tk.END, values=novo_item)
                janela_adicionar.destroy()

            tk.Button(janela_adicionar, text="Salvar", command=salvar_novo).pack(pady=10)

        def editar_item():
            item_selecionado = tree.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um item para editar.")
                return

            valores = tree.item(item_selecionado[0], "values")

            janela_edicao = tk.Toplevel()
            janela_edicao.title("Editar Item")
            janela_edicao.geometry("300x250")
            janela_edicao.resizable(False, False)

            labels = ["Alimento", "Calorias", "Quantidade", "Validade"]
            entradas = []

            for i, label in enumerate(labels):
                tk.Label(janela_edicao, text=label).pack()
                entrada = tk.Entry(janela_edicao)
                entrada.insert(0, valores[i+1])  # Pula o ID
                entrada.pack()
                entradas.append(entrada)

            def salvar_edicao():
                novos_valores = (
                    valores[0],
                    entradas[0].get(),
                    entradas[1].get(),
                    entradas[2].get(),
                    entradas[3].get()
                )
                tree.item(item_selecionado[0], values=novos_valores)
                janela_edicao.destroy()

            tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).pack(pady=10)

        def excluir_item():
            item_selecionado = tree.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um item para excluir.")
                return

            confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este item?")
            if confirmar:
                tree.delete(item_selecionado[0])

        frame_botoes = tk.Frame(janela_cardapio)
        frame_botoes.place(x=100, y=365)

        btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar_item, width=10)
        btn_adicionar.grid(row=0, column=0, padx=10)

        btn_editar = tk.Button(frame_botoes, text="Editar", command=editar_item, width=10)
        btn_editar.grid(row=0, column=1, padx=10)

        btn_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir_item, width=10)
        btn_excluir.grid(row=0, column=2, padx=10)

        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=janela_cardapio.destroy, width=10)
        btn_voltar.grid(row=0, column=3, padx=10)
        
Application()
