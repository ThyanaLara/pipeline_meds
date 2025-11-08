import pandas as pd
import pdfplumber
import os
import re

# Caminho do PDF
pdf_path = r'C:\meds_pipeline\data\0_raw\BRASINDICE_PF.pdf'
# Lista para armazenar os dados
dados = []

# Função para extrair dados do PDF seguindo lógica de layout
def extrair_dados_linha(linha):
    try:
        # Captura o Código TISS (10 dígitos) e o Código TUSS (até 8 dígitos), separados por espaços
        match = re.match(r'^(\d{10})\s+(\d{0,8})\s+(.*)', linha)
        if not match:
            return None

        codigo_tiss = match.group(1).strip()
        codigo_tuss = match.group(2).strip()
        restante = match.group(3).strip()

        # Encontrar o valor: último número com vírgula, seguido ou não de "REAL"
        match_valor = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2,4})\s*(REAL)?$', restante)
        if match_valor:
            valor = match_valor.group(1).replace('.', '').replace(',', '.')
            cobranca = match_valor.group(2) if match_valor.group(2) else ''
            texto_antes_valor = restante[:match_valor.start()].rstrip()

            # Laboratório: última palavra antes do valor
            partes = texto_antes_valor.rsplit(' ', 1)
            if len(partes) == 2:
                produto = partes[0].strip()
                laboratorio = partes[1].strip()
            else:
                produto = texto_antes_valor
                laboratorio = ''

            return [codigo_tiss, codigo_tuss, produto, laboratorio, valor, cobranca]
        else:
            return None
    except Exception as e:
        return None
    

# Percorre o arquivo PDF e aplica a função para extrair texto completo da página

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[:288]:  # quantidade de paginas
        linhas = page.extract_text().split('\n')
        for linha in linhas:
            if linha.strip() and re.match(r'^\d{10}', linha):  # Linha válida começa com 10 dígitos
                dados_linha = extrair_dados_linha(linha)
                if dados_linha:
                    dados.append(dados_linha)

# Criar DataFrame
colunas = ['codigo_tiss', 'codigo_tuss', 'produto', 'laboratorio', 'valor', 'cobranca']
df = pd.DataFrame(dados, columns=colunas)

df['valor'] = df['valor'].astype(float)

df.to_csv(r'C:\meds_pipeline\data\1_trusted\tabala_brasindice.csv',index=False)