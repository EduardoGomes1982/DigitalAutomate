"""Regra central de qualidade: avalia se uma peca esta aprovada ou reprovada."""

PESO_MIN = 95.0
PESO_MAX = 105.0
CORES_PERMITIDAS = {"azul", "verde"}
COMPRIMENTO_MIN = 10.0
COMPRIMENTO_MAX = 20.0


def avaliar_peca(peca):
    motivos = []
    if not PESO_MIN <= peca["peso"] <= PESO_MAX:
        motivos.append("peso fora da faixa")
    if peca["cor"] not in CORES_PERMITIDAS:
        motivos.append("cor nao permitida")
    if not COMPRIMENTO_MIN <= peca["comprimento"] <= COMPRIMENTO_MAX:
        motivos.append("comprimento fora do intervalo")
    return {"aprovada": len(motivos) == 0, "motivos": motivos}