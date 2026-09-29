from database import get_db_connection


def listar_servicos():
    connection = get_db_connection()
    try:
        return connection.execute(
            """
            SELECT servicos.*,
                   veiculos.placa, veiculos.modelo,
                   clientes.nome AS cliente_nome,
                   servicos_disponiveis.nome AS servico_nome
            FROM servicos
            JOIN veiculos ON veiculos.id = servicos.veiculo_id
            JOIN clientes ON clientes.id = veiculos.cliente_id
            JOIN servicos_disponiveis
                ON servicos_disponiveis.id = servicos.servico_disponivel_id
            ORDER BY servicos.data DESC, servicos.id DESC
            """
        ).fetchall()
    finally:
        connection.close()


def buscar_servico(servico_id):
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM servicos WHERE id = ?", (servico_id,)
        ).fetchone()
    finally:
        connection.close()


def criar_servico(veiculo_id, servico_disponivel_id, preco, data, observacao):
    connection = get_db_connection()
    try:
        connection.execute(
            """
            INSERT INTO servicos
                (veiculo_id, servico_disponivel_id, preco, data, observacao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (veiculo_id, servico_disponivel_id, preco, data, observacao),
        )
        connection.commit()
    finally:
        connection.close()


def atualizar_servico(servico_id, veiculo_id, servico_disponivel_id, preco, data, observacao):
    connection = get_db_connection()
    try:
        connection.execute(
            """
            UPDATE servicos
            SET veiculo_id = ?, servico_disponivel_id = ?, preco = ?, data = ?, observacao = ?
            WHERE id = ?
            """,
            (veiculo_id, servico_disponivel_id, preco, data, observacao, servico_id),
        )
        connection.commit()
    finally:
        connection.close()


def excluir_servico(servico_id):
    connection = get_db_connection()
    try:
        connection.execute("DELETE FROM servicos WHERE id = ?", (servico_id,))
        connection.commit()
    finally:
        connection.close()
