# Desafio de Automação Digital

**Gestão de Peças, Qualidade e Armazenamento**

> Protótipo em Python que representa o fluxo industrial de inspeção, aprovação e armazenamento de peças, com regras de qualidade explícitas, controle de caixas de capacidade limitada e relatórios consolidados.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)
![Disciplina](https://img.shields.io/badge/Disciplina-Algoritmos%20e%20L%C3%B3gica-lightgrey)

---

## Sumário

- [Visão Geral](#visão-geral)
- [Objetivos](#objetivos)
- [Funcionalidades](#funcionalidades)
- [Regras de Negócio](#regras-de-negócio)
- [Como Funciona](#como-funciona)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Como Rodar](#como-rodar)
- [Publicação no GitHub](#publicação-no-github)
- [Usando o Menu](#usando-o-menu)
- [Exemplos de Entrada e Saída](#exemplos-de-entrada-e-saída)
- [Persistência dos Dados](#persistência-dos-dados)
- [Tratamento de Entrada](#tratamento-de-entrada)
- [Solução de Problemas](#solução-de-problemas)
- [Evoluções Futuras](#evoluções-futuras)
- [Licença](#licença)
- [Autor](#autor)

---

## Visão Geral

Em uma linha de montagem, cada peça precisa ser medida, decidida, registrada e destinada. A inspeção manual acumula variabilidade: atrasos, falhas de conferência, custo de retrabalho e critérios inconsistentes entre operadores.

Este projeto converte as regras operacionais em um procedimento computacional repetível. O programa recebe os dados de cada peça (id, peso, cor e comprimento), aplica automaticamente os critérios de qualidade, armazena as peças aprovadas em caixas de 10 unidades e gera um relatório final com totais, motivos de reprovação e uso de caixas.

A proposta segue o enunciado do trabalho da disciplina **Algoritmos e Lógica de Programação**, com código em Python puro, sem dependências externas, usando funções, condicionais, laços e estruturas de dados (dicionários e listas) para representar o fluxo industrial.

## Objetivos

**Objetivo geral:** construir um protótipo em Python que represente o fluxo industrial de forma lógica, modular e verificável.

**Objetivos específicos:**

1. Compreender os gargalos do processo manual de inspeção.
2. Estruturar as decisões de qualidade em uma regra central explícita.
3. Processar múltiplas peças em um laço principal com entrada validada.
4. Controlar o acondicionamento em caixas de capacidade fixa.
5. Produzir informação gerencial por meio do relatório consolidado.

## Funcionalidades

- [x] Cadastrar nova peça com validação de entrada (id único, peso, cor e comprimento)
- [x] Avaliar automaticamente aprovação ou reprovação pelos três critérios simultâneos
- [x] Registrar todos os motivos de reprovação de cada peça
- [x] Armazenar peças aprovadas em caixas de 10 unidades
- [x] Fechar a caixa ao atingir a capacidade e abrir uma nova
- [x] Listar peças aprovadas e reprovadas com seus atributos e motivos
- [x] Remover peça cadastrada (atualizando as caixas)
- [x] Listar caixas com status (fechada ou em uso)
- [x] Gerar relatório final consolidado
- [x] Persistir o estado em JSON para retomar a sessão depois

## Regras de Negócio

A aprovação exige que **os três critérios sejam verdadeiros ao mesmo tempo**. Nenhum critério compensa outro.

| Critério    | Faixa permitida | Observação                                    |
| ----------- | --------------- | --------------------------------------------- |
| Peso        | 95 g a 105 g    | Intervalo fechado, limites inclusivos         |
| Cor         | azul ou verde   | Conjunto permitido, normalizado em minúsculas |
| Comprimento | 10 cm a 20 cm   | Intervalo fechado, limites inclusivos         |

**Armazenamento:**

- Capacidade fixa de **10 peças por caixa**.
- Ao atingir 10 peças, a caixa é fechada (status `completa`) e a próxima abertura cria uma nova caixa.
- Uma caixa parcial ao final da sessão permanece válida e é exibida como **em uso**.

**Observações importantes:**

> Uma peça pode acumular **mais de um motivo** de reprovação, por isso a soma das ocorrências por causa pode superar o total de peças reprovadas.

> **Entrada inválida é diferente de peça reprovada.** Dados malformados são rejeitados na captura; a reprovação é uma decisão de qualidade sobre dados válidos.

> Lembrete: valores exatamente nos limites (95 g, 105 g, 10 cm, 20 cm) são **aprovados**.

## Como Funciona

O fluxo de dados percorre cinco etapas: captura, validação, avaliação, armazenamento e relatório.

### 1) Captura e validação de entrada

O módulo `entrada.py` lê os valores e rejeita campos vazios, IDs duplicados e números inválidos, permitindo nova tentativa sem quebrar o lote:

```python
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
```

### 2) Avaliação de qualidade

O módulo `qualidade.py` centraliza a regra e não para no primeiro erro. Cada verificação independente acrescenta uma causa à lista de motivos:

```python
def avaliar_peca(peca):
    motivos = []
    if not PESO_MIN <= peca["peso"] <= PESO_MAX:
        motivos.append("peso fora da faixa")
    if peca["cor"] not in CORES_PERMITIDAS:
        motivos.append("cor nao permitida")
    if not COMPRIMENTO_MIN <= peca["comprimento"] <= COMPRIMENTO_MAX:
        motivos.append("comprimento fora do intervalo")
    return {"aprovada": len(motivos) == 0, "motivos": motivos}
```

### 3) Armazenamento em caixas

O módulo `armazenamento.py` mantém a invariante de que a caixa nunca ultrapassa 10 peças:

```python
def armazenar(peca, caixa_atual, caixas):
    if caixa_atual is None:
        caixa_atual = {"numero": len(caixas) + 1, "pecas": [], "status": "aberta"}
        caixas.append(caixa_atual)
    caixa_atual["pecas"].append(peca["id"])
    if len(caixa_atual["pecas"]) == CAPACIDADE_CAIXA:
        caixa_atual["status"] = "completa"
        return None  # caixa fechou; a proxima peca abre outra
    return caixa_atual
```

Ao remover uma peça, ela é retirada da caixa correspondente; se a caixa ficar vazia, ela é removida e as demais são renumeradas.

### 4) Relatório consolidado

O módulo `relatorio.py` lê o estado acumulado, sem recalcular decisões. A contagem de motivos percorre as peças reprovadas e incrementa os contadores por causa:

```python
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
```

## Estrutura do Projeto

```text
desafio-automacao-digital/
├── src/
│   └── desafio_automacao/
│       ├── __init__.py
│       ├── main.py              # menu principal e composição das operações
│       ├── qualidade.py         # avaliar_peca, constantes da regra de qualidade
│       ├── armazenamento.py     # armazenar, controle de caixas
│       ├── relatorio.py         # gerar_relatorio consolidado
│       ├── entrada.py           # leitura e validação de dados de entrada
│       └── persistencia.py      # salvar e carregar estado em JSON
├── README.md
└── .gitignore
```

| Módulo             | Responsabilidade               | Principais funções                                                                            |
| ------------------ | ------------------------------ | --------------------------------------------------------------------------------------------- |
| `main.py`          | Menu interativo e orquestração | `main`, `cadastrar_peca`, `listar_pecas`, `remover_peca`, `listar_caixas`, `exibir_relatorio` |
| `qualidade.py`     | Regra central de aprovação     | `avaliar_peca`                                                                                |
| `armazenamento.py` | Caixas de 10 peças             | `armazenar`, `caixa_atual_de`, `retirar_da_caixa`                                             |
| `relatorio.py`     | Consolidação dos resultados    | `gerar_relatorio`                                                                             |
| `entrada.py`       | Entrada validada               | `ler_numero`, `ler_cor`, `ler_id`, `id_existe`                                                |
| `persistencia.py`  | Persistência em JSON           | `salvar_estado`, `carregar_estado`                                                            |

## Requisitos

- **Python 3.8 ou superior** (testado na 3.11).
- **Nenhuma dependência externa**: o projeto usa apenas a biblioteca padrão (`json`, `pathlib`, `float`/`input`).

## Como Rodar

### Passo a passo

1. Extraia ou clone o projeto em uma pasta.
2. Abra o terminal (VSCode: `Ctrl+J` no Windows/Linux, `Cmd+J` no Mac).
3. Entre na pasta `src` do projeto.
4. Execute o programa.

**Linux / macOS:**

```bash
cd desafio-automacao-digital/src
python3 -m desafio_automacao.main
```

**Windows (PowerShell):**

```powershell
cd desafio-automacao-digital\src
python -m desafio_automacao.main
```

> Se preferir rodar a partir da raiz do projeto, aponte o `PYTHONPATH` para `src`. Exemplo no Linux/macOS: `PYTHONPATH=src python3 -m desafio_automacao.main`.

Na primeira execução, o programa abre o menu e cria o arquivo `dados_automacao.json` na pasta atual quando a primeira peça for cadastrada.

## Publicação no GitHub

O trabalho exige um repositório com o código fonte. Crie um repositório vazio no GitHub (sem README inicial) e depois execute:

```bash
git init
git add .
git commit -m "Projeto: Desafio de Automacao Digital"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/desafio-automacao-digital.git
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu nome de usuário no GitHub. O arquivo `.gitignore` impede o envio de `__pycache__/` e do `dados_automacao.json` gerado localmente.

## Usando o Menu

Ao executar o programa, o menu é exibido:

```text
===== DESAFIO DE AUTOMACAO DIGITAL =====
1. Cadastrar nova peca
2. Listar pecas aprovadas/reprovadas
3. Remover peca cadastrada
4. Listar caixas
5. Gerar relatorio final
0. Sair
Escolha uma opcao:
```

| Opção | Ação                  | Efeito                                                               |
| ----- | --------------------- | -------------------------------------------------------------------- |
| `1`   | Cadastrar nova peça   | Valida os dados, avalia a qualidade, armazena ou registra reprovação |
| `2`   | Listar peças          | Mostra aprovadas e reprovadas com atributos e motivos                |
| `3`   | Remover peça          | Remove peça e atualiza as caixas                                     |
| `4`   | Listar caixas         | Mostra todas as caixas com status (fechada ou em uso)                |
| `5`   | Gerar relatório final | Consolida totais, motivos e caixas                                   |
| `0`   | Sair                  | Salva o estado e encerra                                             |

## Exemplos de Entrada e Saída

### Exemplo 1: peça aprovada

```text
Escolha uma opcao: 1
Id da peca: P1
Peso (g): 100
Cor da peca (azul/verde/outra): azul
Comprimento (cm): 15
Peca P1: APROVADA. Armazenada na caixa 1.
```

### Exemplo 2: peça reprovada com um motivo

```text
Escolha uma opcao: 1
Id da peca: P2
Peso (g): 110
Cor da peca (azul/verde/outra): verde
Comprimento (cm): 12
Peca P2: REPROVADA. Motivos: peso fora da faixa.
```

### Exemplo 3: peça reprovada com dois motivos

```text
Escolha uma opcao: 1
Id da peca: P3
Peso (g): 90
Cor da peca (azul/verde/outra): vermelha
Comprimento (cm): 12
Peca P3: REPROVADA. Motivos: peso fora da faixa, cor nao permitida.
```

### Exemplo 4: listar caixas (fechada e em uso)

Após 11 peças aprovadas (10 fecham a caixa 1, a 11ª abre a caixa 2):

```text
Escolha uma opcao: 4
Caixa 1: FECHADA | 10/10 pecas | ids: P1, P2, P3, P4, P5, P6, P7, P8, P9, P10
Caixa 2: EM USO | 1/10 pecas | ids: P11
```

### Exemplo 5: relatório final

```text
Escolha uma opcao: 5
=== RELATORIO FINAL ===
Pecas aprovadas: 2
Pecas reprovadas: 3
Motivos de reprovacao:
  - cor nao permitida: 2
  - comprimento fora do intervalo: 1
  - peso fora da faixa: 1
Caixas utilizadas: 1 (0 completas, 1 parciais)
Obs.: uma peca pode ter mais de um motivo; por isso as ocorrencias por causa podem superar o total de reprovadas.
```

No exemplo acima, as 3 peças reprovadas geraram 4 ocorrências de motivo (a peça P3 contribuiu com 2), o que explica a soma superior ao total de reprovadas.

## Persistência dos Dados

O estado é salvo automaticamente em **`dados_automacao.json`** após cada operação que altera os dados (cadastro, remoção e saída). Ao iniciar, o programa carrega a sessão anterior automaticamente:

```text
Sessao anterior carregada de dados_automacao.json.
```

O JSON tem esta forma:

```json
{
  "aprovadas": [
    {
      "id": "P1",
      "peso": 100.0,
      "cor": "azul",
      "comprimento": 15.0,
      "motivos": []
    }
  ],
  "reprovadas": [],
  "caixas": [{ "numero": 1, "pecas": ["P1"], "status": "aberta" }]
}
```

A versão inicial mantinha os dados ~~somente em memória~~ durante a sessão; a persistência em JSON foi adicionada para permitir retomar o trabalho depois do fechamento do programa. Se o arquivo estiver corrompido, o programa recomeça com estado vazio em vez de falhar.

## Tratamento de Entrada

- Campos vazios são rejeitados com mensagem clara.
- Números aceitam ponto ou vírgula decimal (`100.5` ou `100,5`).
- Cores são normalizadas para minúsculas.
- IDs duplicados são rejeitados.
- Opções de menu fora do intervalo (0 a 5) mostram aviso.
- Erro de entrada não vira laço infinito nem encerra o programa.

## Solução de Problemas

| Problema                                                   | Causa provável                                    | Solução                                             |
| ---------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------- |
| `ModuleNotFoundError: No module named 'desafio_automacao'` | Executou fora da pasta `src`, ou sem `PYTHONPATH` | Execute `cd src` antes, ou use `PYTHONPATH=src`     |
| Relatório mostra peças de outra sessão                     | Estado carregado de `dados_automacao.json`        | Exclua o arquivo para começar do zero               |
| Arquivo JSON corrompido                                    | Edição manual do arquivo                          | Apague o arquivo ou restaure do GitHub              |
| Programa fecha sem salvar                                  | O programa salva a cada operação mutável          | Verifique se a pasta atual tem permissão de escrita |

## Evoluções Futuras

O protótipo segue os princípios de **modularidade, rastreabilidade e controle de estado**, o que permite crescer sem reescrever a regra central:

- [ ] Adicionar suíte de testes automatizados (pytest) para limites e transições de caixa
- [ ] Substituir a persistência JSON por banco de dados (SQLite)
- [ ] Receber medições de sensores (célula de carga, leitor óptico, RFID)
- [ ] Integrar com CLP, esteira e sistemas SCADA/MES
- [ ] Aplicar visão computacional e modelos preditivos na inspeção

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo `LICENSE` para os detalhes completos.

## Autor

**Eduardo Gomes**  
Acadêmico em Tecnologias com IA e Desenvolvimento No-Code e Low-Code na UNIFECAF  
Disciplina: **Algoritmos e Lógica de Programação**

**Fonte de pesquisa:**[^1]

[^1]: Documentação oficial da linguagem: https://docs.python.org/3/ e comunidade brasileira: https://python.org.br/.

O README cobre tudo que o enunciado pede: explicação do funcionamento, passo a passo para rodar e exemplos de entrada e saída reais, além de estrutura, regras, persistência e publicação no GitHub. Se quiser, o próximo passo natural é o roteiro do vídeo pitch.
