from condoAccess.database.database import criar_banco
from condoAccess.visitantes import cadastrar_visitante, listar_visitantes
from condoAccess.visitas import registrar_entrada_por_rg, registrar_saida_por_rg, buscar_visitante_por_rg, listar_visitas




def menu_principal():
    criar_banco() # Garante que o banco e as tabelas existam

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Cadastrar visitante")
        print("2. Listar visitantes")
        print("3. Registrar entrada")
        print("4. Registrar saída")
        print("5. Listar visitas")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            rg = input("RG: ")
            telefone = input("Telefone (opcional): ")
            cadastrar_visitante(nome, rg, telefone)
        elif escolha == '2':
            listar_visitantes()
        elif escolha == '3':
            print("Registrar entrada de visitante")
            rg = input("RG do visitante: ")
            unidade = input("Unidade: ")
            registrar_entrada_por_rg(rg, unidade)
        elif escolha == '4':
            print("Registrar saída de visitante")
            rg = input("RG do visitante: ")
            registrar_saida_por_rg(rg)
        elif escolha == '5':
            listar_visitas()
        elif escolha == '0':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
