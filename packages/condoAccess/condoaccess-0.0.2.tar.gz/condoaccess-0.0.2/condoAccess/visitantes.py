import sqlite3

def cadastrar_visitante(nome, rg, telefone=None):
    """Insere um visitante no banco de dados."""
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO visitantes (nome, rg, telefone) 
        VALUES (?, ?, ?);
        ''', (nome, rg, telefone))
        conn.commit()
        print("Visitante cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("O RG já está cadastrado. Registre apenas a entrada do visitante.")
    finally:
        conn.close()

def listar_visitantes():
    """Lista todos os visitantes cadastrados."""
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM visitantes;')
    visitantes = cursor.fetchall()

    for visitante in visitantes:
        print(visitante)

    conn.close()