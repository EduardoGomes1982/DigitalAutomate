"""Menu principal e composicao do sistema."""

from start.armazenamento import armazenar, caixa_atual_de, retirar_da_caixa
from start.entrada import ler_cor, ler_id, ler_numero
from start.persistencia import carregar_estado, salvar_estado
from start.qualidade import avaliar_peca
from start.relatorio import gerar_relatorio


def cadastrar_peca(aprovadas, reprovadas, caixas, caixa_atual):
    print("\n--- CADASTRAR NOVA PECA ---")
    peca_id = ler_id(aprovadas, reprovadas)
    peso = ler_numero("Peso (g): ")
    cor = ler_cor()
    comprimento = ler_numero("Comprimento (cm): ")

    peca = {"id": peca_id, "peso": peso, "cor": cor, "comprimento": comprimento}
    resultado = avaliar_peca(peca)
    peca["motivos"] = resultado["motivos"]

    if resultado["aprovada"]:
        aprovadas.append(peca)
        caixa_atual = armazenar(peca, caixa_atual, caixas)
        print(f"Peca {peca_id}: APROVADA. Armazenada na caixa {caixas[-1]['numero']}.")
    else:
        reprovadas.append(peca)
        print(f"Peca {peca_id}: REPROVADA. Motivos: {', '.join(peca['motivos'])}.")
    return caixa_atual


def listar_pecas(aprovadas, reprovadas):
    if not aprovadas and not reprovadas:
        print("Nenhuma peca cadastrada ainda.")
        return
    if aprovadas:
        print("\nAPROVADAS:")
        for peca in aprovadas:
            print(f"  id={peca['id']} | peso={peca['peso']}g | cor={peca['cor']} "
                  f"| comprimento={peca['comprimento']}cm")
    if reprovadas:
        print("\nREPROVADAS:")
        for peca in reprovadas:
            print(f"  id={peca['id']} | peso={peca['peso']}g | cor={peca['cor']} "
                  f"| comprimento={peca['comprimento']}cm "
                  f"| motivos={', '.join(peca['motivos'])}")


def remover_peca(aprovadas, reprovadas, caixas):
    peca_id = input("Id da peca a remover: ").strip()
    for peca in aprovadas:
        if peca["id"] == peca_id:
            aprovadas.remove(peca)
            retirar_da_caixa(peca_id, caixas)
            print(f"Peca {peca_id} removida (aprovada).")
            return
    for peca in reprovadas:
        if peca["id"] == peca_id:
            reprovadas.remove(peca)
            print(f"Peca {peca_id} removida (reprovada).")
            return
    print(f"Peca {peca_id} nao encontrada.")


def listar_caixas(caixas):
    if not caixas:
        print("Nenhuma caixa utilizada ainda.")
        return
    for caixa in caixas:
        rotulo = "FECHADA" if caixa["status"] == "completa" else "EM USO"
        ids = ", ".join(caixa["pecas"]) if caixa["pecas"] else "-"
        print(f"Caixa {caixa['numero']}: {rotulo} | "
              f"{len(caixa['pecas'])}/{CAPACIDADE_CAIXA} pecas | ids: {ids}")


def exibir_relatorio(aprovadas, reprovadas, caixas):
    relatorio = gerar_relatorio(aprovadas, reprovadas, caixas)
    print("\n=== RELATORIO FINAL ===")
    print(f"Pecas aprovadas: {relatorio['aprovadas']}")
    print(f"Pecas reprovadas: {relatorio['reprovadas']}")
    if relatorio["motivos"]:
        print("Motivos de reprovacao:")
        for motivo, quantidade in sorted(relatorio["motivos"].items()):
            print(f"  - {motivo}: {quantidade}")
    print(f"Caixas utilizadas: {relatorio['caixas']} "
          f"({relatorio['completas']} completas, {relatorio['parciais']} parciais)")
    print("Obs.: uma peca pode ter mais de um motivo; por isso as ocorrencias "
          "por causa podem superar o total de reprovadas.")


def menu():
    print("\n===== DESAFIO DE AUTOMACAO DIGITAL =====")
    print("1. Cadastrar nova peca")
    print("2. Listar pecas aprovadas/reprovadas")
    print("3. Remover peca cadastrada")
    print("4. Listar caixas")
    print("5. Gerar relatorio final")
    print("0. Sair")


def main():
    aprovadas, reprovadas, caixas = carregar_estado()
    caixa_atual = caixa_atual_de(caixas)
    if aprovadas or reprovadas or caixas:
        print("Sessao anterior carregada de dados_automacao.json.")

    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            caixa_atual = cadastrar_peca(aprovadas, reprovadas, caixas, caixa_atual)
            salvar_estado(aprovadas, reprovadas, caixas)
        elif opcao == "2":
            listar_pecas(aprovadas, reprovadas)
        elif opcao == "3":
            remover_peca(aprovadas, reprovadas, caixas)
            salvar_estado(aprovadas, reprovadas, caixas)
        elif opcao == "4":
            listar_caixas(caixas)
        elif opcao == "5":
            exibir_relatorio(aprovadas, reprovadas, caixas)
        elif opcao == "0":
            salvar_estado(aprovadas, reprovadas, caixas)
            print("Dados salvos. Encerrando o programa. Ate logo!")
            break
        else:
            print("Opcao invalida. Escolha um numero de 0 a 5.")


if __name__ == "__main__":
    main()