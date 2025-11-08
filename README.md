# Med Data Cleaning — BRASINDICE

Objetivo: limpar e padronizar dados de medicamentos (nomes, dosagens e unidades) a partir de fontes “do mundo real”, usando o BRASÍNDICE como exemplo público.

## Como reproduzir
1. Coloque `BRASINDICE_PF.pdf` em `data/raw/`.
2. Abra os notebooks em `notebooks/`:
   - `01_extracao_brasindice.ipynb`
   - `02_tratamento_medicamentos.ipynb`

## Estrutura (resumo)
- `data/raw/`: arquivos brutos (PDFs, CSVs)
- `data/interim/`: dados intermediários
- `data/processed/`: dados finais (CSV/Parquet)
- `notebooks/`: exploração e demonstração
- `src/`: funções reutilizáveis (em breve)

