import sqlite3

DATABASE_NAME = "database.db"


def get_db_connection():
    """Abre uma conexão simples com o banco SQLite."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    # O SQLite só respeita chaves estrangeiras (FOREIGN KEY) se pedirmos.
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    """Cria as tabelas iniciais se elas ainda não existirem."""
    connection = get_db_connection()
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL REFERENCES clientes (id),
            placa TEXT NOT NULL UNIQUE,
            modelo TEXT NOT NULL,
            cor TEXT
        );

        -- Catálogo: os serviços que o lava rápido oferece.
        CREATE TABLE IF NOT EXISTS servicos_disponiveis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL,
            descricao TEXT
        );

        -- Serviços realizados: liga um veículo a um serviço do catálogo.
        -- O preço é copiado para cá para o histórico não mudar se o catálogo mudar.
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL REFERENCES veiculos (id),
            servico_disponivel_id INTEGER NOT NULL REFERENCES servicos_disponiveis (id),
            preco REAL NOT NULL,
            data TEXT NOT NULL DEFAULT CURRENT_DATE,
            observacao TEXT
        );
        """
    )
    connection.commit()
    connection.close()
