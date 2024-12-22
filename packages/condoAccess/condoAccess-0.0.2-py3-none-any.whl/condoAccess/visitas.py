import sqlite3


def buscar_visitante_por_rg(rg):
    """Busca o ID do visitante pelo RG informado."""
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, nome, telefone FROM visitantes WHERE rg = ?;', (rg,))
    visitante = cursor.fetchone() # Retorna o visitante ou None

    conn.close()
    return visitante

def registrar_entrada_por_rg(rg, unidade):
    """Registra a entrada de um visitante com base no RG."""
    visitante = buscar_visitante_por_rg(rg)

    if visitante is None:
        print("Visitante não encontrado! Certifique-se de que ele esteja cadastrado.")
        return

    visitante_id, nome, telefone = visitante
    print(f"Visitante encontrado: {nome} (Telefone: {telefone})")

    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO visitas (visitante_id, unidade) 
    VALUES (?, ?);
    ''', (visitante_id, unidade))
    conn.commit()
    conn.close()

    print("Entrada registrada com sucesso!") 

def registrar_saida_por_rg(rg):
    """Registra a saída de um visitante com base no RG."""
    visitante = buscar_visitante_por_rg(rg)

    if visitante is None:
        print("Visitante não encontrado! Certifique-se de que ele esteja cadastrado.")
        return

    visitante_id, nome, _ = visitante
    print(f"Visitante encontrado: {nome}")

    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    # Localiza a visita ativa do visitante (sem saída registrada)
    cursor.execute('''
    SELECT id 
    FROM visitas 
    WHERE visitante_id = ? AND data_hora_saida IS NULL
    ORDER BY data_hora_entrada DESC
    LIMIT 1;
    ''', (visitante_id,))
    visita = cursor.fetchone()

    if visita is None:
        print("Nenhuma visita ativa encontrada para esse visitante.")
        conn.close()
        return

    visita_id = visita[0]

    # Atualiza o registro de saída
    cursor.execute('''
    UPDATE visitas
    SET data_hora_saida = CURRENT_TIMESTAMP
    WHERE id = ?;
    ''', (visita_id,))
    conn.commit()
    conn.close()

    print("Saída registrada com sucesso!")

def listar_visitas():
 with sqlite3.connect('portaria.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT visitas.id, visitantes.nome, visitas.unidade, 
                   visitas.data_hora_entrada, visitas.data_hora_saida
            FROM visitas
            INNER JOIN visitantes ON visitas.visitante_id = visitantes.id
            ORDER BY visitas.data_hora_entrada DESC
            LIMIT 50
        ''')
        visitas = cursor.fetchall()

        if not visitas:
            print("Nenhuma visita registrada.")
            return

        print("Últimas visitas registradas:")
        print("-" * 50)
        for visita in visitas:
            print(f"ID da Visita: {visita[0]}")
            print(f"Nome do Visitante: {visita[1]}")
            print(f"Unidade Visitada: {visita[2]}")
            print(f"Data e Hora de Entrada: {visita[3]}")
            print(f"Data e Hora de Saída: {visita[4] if visita[4] else 'Ainda não registrado'}")
            print("-" * 50)
                     