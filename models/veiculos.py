import sqlite3

from database import get_db_connection


def listar_veiculos():
    connection = get_db_connection()
    try:
        # JOIN traz o nome do cliente junto com cada veículo.
        return connection.execute(
            """
            SELECT veiculos.*, clientes.nome AS cliente_nome
            FROM veiculos
            JOIN clientes ON clientes.id = veiculos.cliente_id
            ORDER BY veiculos.placa
            """
        ).fetchall()
    finally:
        connection.close()


def buscar_veiculo(veiculo_id):
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM veiculos WHERE id = ?", (veiculo_id,)
        ).fetchone()
    finally:
        connection.close()


def criar_veiculo(cliente_id, placa, modelo, cor):
    """Retorna False se a placa já estiver cadastrada."""
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO veiculos (cliente_id, placa, modelo, cor) VALUES (?, ?, ?, ?)",
            (cliente_id, placa, modelo, cor),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def atualizar_veiculo(veiculo_id, cliente_id, placa, modelo, cor):
    """Retorna False se a placa já pertencer a outro veículo."""
    connection = get_db_connection()
    try:
        connection.execute(
            "UPDATE veiculos SET cliente_id = ?, placa = ?, modelo = ?, cor = ? WHERE id = ?",
            (cliente_id, placa, modelo, cor, veiculo_id),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def excluir_veiculo(veiculo_id):
    """Retorna False se o veículo já tiver serviços realizados."""
    connection = get_db_connection()
    try:
        connection.execute("DELETE FROM veiculos WHERE id = ?", (veiculo_id,))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()
