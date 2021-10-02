from flask import Flask, make_response, request, render_template, redirect, send_from_directory
from contextlib import closing
import sqlite3
import os
import werkzeug

app = Flask(__name__)

@app.route("/")
@app.route("/morador/novo")
@app.route("/condominio/novo")
@app.route("/funcionario/novo")
@app.route("/login")
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

def conectar():
    return sqlite3.connect('Condominio.sdb')

def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        con.commit()
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