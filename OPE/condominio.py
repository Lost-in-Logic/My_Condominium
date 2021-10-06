from flask import Flask, make_response, request, render_template, redirect, send_from_directory
from contextlib import closing
import sqlite3
import os
import werkzeug

app = Flask(__name__)


@app.route("/funcionario/novo")
def funcionario():
    return render_template("form_funcionario.html")

@app.route("/funcionario/novo", methods=['POST'])
def criar_funcionario():
    formulario = request.form
    nome = formulario['nome']
    cpf = formulario['cpf']
    dtnasc = formulario['dtnasc']
    profissao = formulario['profissao']
    contato = formulario['contato']
    codigo = db_criarfuncionario(nome, cpf, dtnasc, profissao, contato)
    return render_template("menu.html", mensagem = f'O funcionário com o código {codigo} foi criado com sucesso.')


@app.route("/login")
@app.route("/")
@app.route("/morador/novo")
def morador():
    return render_template("form_morador.html")

@app.route("/morador/novo", methods = ['POST'])
def criar_morador():
    formulario = request.form
    nome = formulario['nome']
    cpf = formulario['cpf']
    rg = formulario['rg']
    apartamento = formulario['apartamento']
    bloco = formulario['bloco']
    dtnasc = formulario['dtnasc']
    contato = formulario['contato']
    email = formulario['email']
    numvaga = formulario['numvaga']
    cad = db_criarmorador(nome, cpf, rg, apartamento, bloco, dtnasc, contato, email, numvaga)
    if cad == True:
        return render_template('menu.html', mensagem = f'O morador {nome} foi cadastrado com sucesso.')
    else:
        return render_template('menu.html', mensagem = f'Ocorreu um eerro durante o cadastro.')

@app.route("/condominio/novo")
def condominio():
    return render_template("form_condominio.html")
app.route("/condominio/novo", methods = ['POST'])
def criar_condominio():
    formulario = request.form
    nome = formulario['nome']
    endereco = formulario['endereco']
    cidade = formulario['cidade']
    estado = formulario['estado']
    contato = formulario['contato']
    numeroap = formulario['numeroap']
    codigo = db_criarcondominio(nome, endereco, cidade, estado, contato, numeroap)
    return render_template("menu.html", mensagem = f'O funcionário com o código {codigo} foi criado com sucesso.')

    

def menu():
    return render_template("menu.html")








############################### API
"""""
def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return db_fazer_login(login, senha)
"""
##################################################### BD

def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

#########################################################

sql_create = """
CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    dtnasc DATE NOT NULL,
    profissao VARCHAR(50) NOT NULL,
    contato VARCHAR(100) NOT NULL,
    UNIQUE(cpf)
);
"""

def conectar():
    return sqlite3.connect('Condominio.sdb')

def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()

def db_criarfuncionario(nome, cpf, dtnasc, profissao, contato):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('INSERT INTO funcionario (nome, cpf, dtnasc, profissao, contato) VALUES (?,?,?,?,?)', [nome, cpf, dtnasc, profissao, contato])
        codigo = cur.lastrowid
        con.commit()
        return codigo

def db_criarmorador(nome, cpf, rg, apartamento, bloco, dtnasc, contato, email, numvaga):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('INSERT INTO funcionario (nome, cpf, rg, apartamento, bloco, dtnasc, contato, email, numvaga) VALUES (?,?,?,?,?,?,?,?,?)', [nome, cpf, rg, apartamento, bloco, dtnasc, contato, email, numvaga])
        con.commit()
        return

def db_criarcondominio(nome, endereco, cidade, estado, contato, numeroap):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('INSERT INTO funcionario (nome, endereco, cidade, estado, contato, numeroap) VALUES (?,?,?,?,?,?)', [nome, endereco, cidade, estado, contato, numeroap])
        codigo = cur.lastrowid
        con.commit()
        return codigo
"""""
def db_fazer_login(login, senha):
    with closing(conectar()) as con, closing(con.cursor) as cur:
        cur.execute("SELECT u.login, u.senha, u.nome FROM usuario u WHERE u.login = ? AND u.senha = ?", [login, senha])
        return row_to_dict(cur.description, cur.fetchone())
"""""

######################### INIT

if __name__ == "__main__":
    db_inicializar()
    app.run()