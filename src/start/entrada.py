"""Leitura e validacao de entrada, separada da avaliacao de qualidade."""


def ler_numero(mensagem):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        if not valor:
            print("Entrada vazia. Digite um numero.")
            continue
        try:
            return float(valor)
        except ValueError:
            print("Valor invalido. Use ponto ou virgula decimal.")


def ler_cor():
    while True:
        cor = input("Cor da peca (azul/verde/outra): ").strip().lower()
        if cor:
            return cor
        print("Entrada vazia. Digite uma cor.")


def ler_id(aprovadas, reprovadas):
    while True:
        peca_id = input("Id da peca: ").strip()
        if not peca_id:
            print("Entrada vazia. Digite um identificador.")
            continue
        if id_existe(peca_id, aprovadas, reprovadas):
            print(f"Id '{peca_id}' ja cadastrado. Use outro.")
            continue
        return peca_id


def id_existe(peca_id, aprovadas, reprovadas):
    return any(peca["id"] == peca_id for peca in aprovadas + reprovadas)