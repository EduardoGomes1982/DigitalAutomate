"""Consolidacao do estado acumulado em relatorio final."""


def gerar_relatorio(aprovadas, reprovadas, caixas):
    contagem = {}
    for item in reprovadas:
        for motivo in item["motivos"]:
            contagem[motivo] = contagem.get(motivo, 0) + 1
    completas = sum(caixa["status"] == "completa" for caixa in caixas)
    return {
        "aprovadas": len(aprovadas),
        "reprovadas": len(reprovadas),
        "motivos": contagem,
        "caixas": len(caixas),
        "completas": completas,
        "parciais": len(caixas) - completas,
    }