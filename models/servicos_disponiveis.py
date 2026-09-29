import sqlite3

from database import get_db_connection


def listar_servicos_disponiveis():
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM servicos_disponiveis ORDER BY nome"
        ).fetchall()
    finally:
        connection.close()


def buscar_servico_disponivel(servico_disponivel_id):
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM servicos_disponiveis WHERE id = ?", (servico_disponivel_id,)
        ).fetchone()
    finally:
        connection.close()


def criar_servico_disponivel(nome, preco, descricao):
    """Retorna False se já existir um serviço com esse nome."""
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO servicos_disponiveis (nome, preco, descricao) VALUES (?, ?, ?)",
            (nome, preco, descricao),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def atualizar_servico_disponivel(servico_disponivel_id, nome, preco, descricao):
    connection = get_db_connection()
    try:
        connection.execute(
            "UPDATE servicos_disponiveis SET nome = ?, preco = ?, descricao = ? WHERE id = ?",
            (nome, preco, descricao, servico_disponivel_id),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def excluir_servico_disponivel(servico_disponivel_id):
    """Retorna False se o serviço já tiver sido realizado alguma vez."""
    connection = get_db_connection()
    try:
        connection.execute(
            "DELETE FROM servicos_disponiveis WHERE id = ?", (servico_disponivel_id,)
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()
