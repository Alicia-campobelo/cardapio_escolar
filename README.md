# 🥗 Sistema de gerenciamento de cardápio escolar(CustomTkinter + SQLite)

Este projeto é um sistema de login com interface gráfica utilizando **CustomTkinter**, **SQLite** e imagens. Além do login, o sistema permite:

- Cadastro de novos usuários
- Edição e exclusão de perfil
- Tela principal com saudação
- Visualização de um cardápio de alimentos
- Simulação de relatórios semanais
- Edição, adição e exclusão de itens do cardápio (visualmente)

---

## 🖼️ Imagens Utilizadas

As imagens estão localizadas dentro da pasta `img/`:

- `img/f.png` – Ícone da tela de login
- `img/eye.png` – Ícone de "mostrar senha"
- `img/eye_off.png` – Ícone de "ocultar senha"

---

## 📦 Bibliotecas Utilizadas

- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter)
- `tkinter` (nativo do Python)
- `sqlite3` (nativo)
- `Pillow` (`PIL`) para manipular imagens

---

## ▶️ Como executar

1. Certifique-se de ter Python 3 instalado.
2. Instale as dependências (caso ainda não tenha):
   ```bash
   pip install customtkinter pillow
   ```
3. Verifique se as imagens estão na pasta `img/` corretamente:
   ```
   projeto/
   ├── img/
   │   ├── f.png
   │   ├── eye.png
   │   └── eye_off.png
   └── seu_arquivo.py
   ```
4. Execute o script:
   ```bash
   python seu_arquivo.py
   ```

---

## 💡 Funcionalidades

- **Login com verificação no banco de dados**
- **Cadastro de usuário com verificação de unicidade**
- **Botão "Mostrar/Ocultar Senha" com ícones**
- **Tela de boas-vindas com acesso ao cardápio e relatórios**
- **Cardápio com sistema de `Treeview` (tabela interativa)**
- **Relatórios fictícios por dia da semana**
- **CRUD visual nos alimentos do cardápio**

---

## 📁 Banco de Dados

O arquivo `sistema.db` é criado automaticamente e contém duas tabelas:

- `usuarios (id, nome, senha)`
- `alimentos (id, nome, calorias)`

A tabela de `alimentos` começa com alguns alimentos fixos e insere mais dados manualmente via interface.

---

## 🚧 Sobre a modularização

Foi tentado modularizar o projeto (separando a lógica de banco, interface, cadastro, etc.) em arquivos diferentes.  
**No entanto, sempre que o código era separado em módulos, alguma funcionalidade parava de funcionar** — especialmente os botões.
Por isso, o código foi mantido **em um único arquivo** e otimizado o maximo para ficar organizado.

---
