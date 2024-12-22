import sqlite3


def criar_banco():
    """Cria o banco de dados e as tabelas necessárias."""
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    # Criação da tabela 'visitantes'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        rg TEXT UNIQUE NOT NULL,
        telefone TEXT
    );
    ''')

    # Criação da tabela 'visitas'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitante_id INTEGER NOT NULL,
        unidade TEXT NOT NULL,
        data_hora_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_hora_saida DATETIME,
        FOREIGN KEY (visitante_id) REFERENCES visitantes (id)
    );
    ''')

    conn.commit()
    conn.close()

    print("Banco de dados criado com sucesso!")
