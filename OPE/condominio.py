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

@app.route("/funcionario")
def listar_funcionarios():
    funcionarios = db_listar_funcionarios()
    return render_template("funcionarios.html", funcionarios = funcionarios)

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
    codigo = db_criarmorador(nome, cpf, rg, apartamento, bloco, dtnasc, contato, email)
    return render_template('menu.html', mensagem = f'O morador {nome} foi cadastrado com sucesso com o id {codigo}.')

@app.route("/morador")
def listar_moradores():
    moradores = db_listar_moradores()
    return render_template("moradores.html", moradores = moradores)


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
CREATE TABLE IF NOT EXISTS Apartamentos (
    idresidencia INTEGER PRIMARY KEY AUTO INCREMENT,
    numresidencia VARCHAR(50) NOT NULL,
    bloco VARCHAR(50),
    idcond INTEGER REFERENCES Condominios (idcond)
);
CREATE TABLE IF NOT EXISTS AreaComum (
    nome TEXT NOT NULL,
    statusreserva BOOLEAN NOT NULL,
    dtreserva DATETIME,
    idlocador INTEGER REFERENCES Moradores (idmorador),
    idarea INTEGER  PRIMARY KEY NOT NULL,
    idcond INTEGER REFERENCES Condominios (idcond) NOT NULL
);
CREATE TABLE IF NOT EXISTS Condominios (
    idcond INT PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL,
    endereço TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    contato TEXT,
    qtdresidencias NUMERIC NOT NULL
);
CREATE TABLE IF NOT EXISTS Encomendas (
    dtentrega DATETIME NOT NULL,
    retirado BOOLEAN,
    dtretirada DATETIME,
    residencia REFERENCES Apartamentos (numresidencia) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS Funcionarios (
    idfuncionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    dtnasc DATE NOT NULL,
    profissao VARCHAR(50) NOT NULL,
    contato VARCHAR(100) NOT NULL,
    UNIQUE(cpf)
);
CREATE TABLE IF NOT EXISTS Moradores (
    nome TEXT NOT NULL,
    cpf NUMERIC,
    rg NUMERIC,
    apartamento NUMERIC NOT NULL,
    bloco TEXT,
    dtnasc DATE NOT NULL,
    contato  NUMERIC,
    email  TEXT,
    idmorador INTEGER PRIMARY KEY NOT NULL,
    idcond REFERENCES Condominios (idcond)
);
CREATE TABLE IF NOT EXISTS VagasdeCarro (
    numvaga NUMERIC PRIMARY KEY NOT NULL,
    idmorador INTEGER REFERENCES Moradores (idmorador),
    idcond INTEGER REFERENCES Condominios (idcond) 
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
        cur.execute('INSERT INTO Funcionários (nome, cpf, dtnasc, profissao, contato) VALUES (?,?,?,?,?)', [nome, cpf, dtnasc, profissao, contato])
        codigo = cur.lastrowid
        con.commit()
        return codigo

def db_criarmorador(nome, cpf, rg, apartamento, bloco, dtnasc, contato, email):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('INSERT INTO Moradores (nome, cpf, rg, apartamento, bloco, dtnasc, contato, email) VALUES (?,?,?,?,?,?,?,?)', [nome, cpf, rg, apartamento, bloco, dtnasc, contato, email])
        codigo = cur.lastrowid
        con.commit()
        return codigo

def db_criarcondominio(nome, endereco, cidade, estado, contato, numeroap):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('INSERT INTO Condominios (nome, endereco, cidade, estado, contato, numeroap) VALUES (?,?,?,?,?,?)', [nome, endereco, cidade, estado, contato, numeroap])
        codigo = cur.lastrowid
        con.commit()
        return codigo
"""""
def db_fazer_login(login, senha):
    with closing(conectar()) as con, closing(con.cursor) as cur:
        cur.execute("SELECT u.login, u.senha, u.nome FROM usuario u WHERE u.login = ? AND u.senha = ?", [login, senha])
        return row_to_dict(cur.description, cur.fetchone())
"""""

def db_listar_funcionarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('SELECT id_funcionario, nome, cpf, dtnasc, profissao, contato from Funcionários')
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_moradores():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute('SELECT idmorador, nome, cpf, rg, apartamento, bloco, dtnasc, contato, email from Moradores')
        return rows_to_dict(cur.description, cur.fetchall())


######################### INIT

if __name__ == "__main__":
    db_inicializar()
    app.run()