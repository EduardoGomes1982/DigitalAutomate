"""Persistencia do estado em JSON para retomar a sessao depois."""

import json
from pathlib import Path

ARQUIVO_DADOS = Path("dados_automacao.json")


def salvar_estado(aprovadas, reprovadas, caixas):
    estado = {"aprovadas": aprovadas, "reprovadas": reprovadas, "caixas": caixas}
    ARQUIVO_DADOS.write_text(
        json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def carregar_estado():
    if not ARQUIVO_DADOS.exists():
        return [], [], []
    try:
        estado = json.loads(ARQUIVO_DADOS.read_text(encoding="utf-8"))
        return (
            estado.get("aprovadas", []),
            estado.get("reprovadas", []),
            estado.get("caixas", []),
        )
    except (json.JSONDecodeError, OSError):
        return [], [], []