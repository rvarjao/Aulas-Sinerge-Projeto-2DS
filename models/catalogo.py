import sqlite3

from database import get_db_connection


def listar_itens():
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM catalogo ORDER BY nome"
        ).fetchall()
    finally:
        connection.close()


def buscar_item(item_id):
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM catalogo WHERE id = ?", (item_id,)
        ).fetchone()
    finally:
        connection.close()


def criar_item(nome, preco, descricao):
    """Retorna False se já existir um serviço com esse nome."""
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO catalogo (nome, preco, descricao) VALUES (?, ?, ?)",
            (nome, preco, descricao),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def atualizar_item(item_id, nome, preco, descricao):
    connection = get_db_connection()
    try:
        connection.execute(
            "UPDATE catalogo SET nome = ?, preco = ?, descricao = ? WHERE id = ?",
            (nome, preco, descricao, item_id),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def excluir_item(item_id):
    """Retorna False se o serviço já tiver sido realizado alguma vez."""
    connection = get_db_connection()
    try:
        connection.execute(
            "DELETE FROM catalogo WHERE id = ?", (item_id,)
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()
