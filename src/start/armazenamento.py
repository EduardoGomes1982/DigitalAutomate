"""Controle de caixas: capacidade fixa, fechamento automatico e reutilizacao."""

CAPACIDADE_CAIXA = 10


def armazenar(peca, caixa_atual, caixas):
    if caixa_atual is None:
        caixa_atual = {"numero": len(caixas) + 1, "pecas": [], "status": "aberta"}
        caixas.append(caixa_atual)
    caixa_atual["pecas"].append(peca["id"])
    if len(caixa_atual["pecas"]) == CAPACIDADE_CAIXA:
        caixa_atual["status"] = "completa"
        return None  # caixa fechou; a proxima peca abre outra
    return caixa_atual


def caixa_atual_de(caixas):
    if caixas and caixas[-1]["status"] == "aberta":
        return caixas[-1]
    return None


def retirar_da_caixa(peca_id, caixas):
    for caixa in caixas:
        if peca_id in caixa["pecas"]:
            caixa["pecas"].remove(peca_id)
            caixa["status"] = (
                "completa" if len(caixa["pecas"]) == CAPACIDADE_CAIXA else "aberta"
            )
            if not caixa["pecas"]:
                caixas.remove(caixa)
                for indice, restante in enumerate(caixas, start=1):
                    restante["numero"] = indice
            return