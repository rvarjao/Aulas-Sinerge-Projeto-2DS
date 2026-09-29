import sqlite3

from database import get_db_connection


def listar_clientes():
    connection = get_db_connection()
    try:
        return connection.execute("SELECT * FROM clientes ORDER BY nome").fetchall()
    finally:
        connection.close()


def buscar_cliente(cliente_id):
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM clientes WHERE id = ?", (cliente_id,)
        ).fetchone()
    finally:
        connection.close()


def criar_cliente(nome, telefone, email):
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
            (nome, telefone, email),
        )
        connection.commit()
    finally:
        connection.close()


def atualizar_cliente(cliente_id, nome, telefone, email):
    connection = get_db_connection()
    try:
        connection.execute(
            "UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE id = ?",
            (nome, telefone, email, cliente_id),
        )
        connection.commit()
    finally:
        connection.close()


def excluir_cliente(cliente_id):
    """Retorna False se o cliente ainda tiver veículos cadastrados."""
    connection = get_db_connection()
    try:
        connection.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()
