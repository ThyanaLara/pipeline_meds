"""
Script: extract_save_data.py
Author: Thyana Lara
Description: Extracts structured medication data from BRASÍNDICE PDF using regex and text parsing.
"""

import pandas as pd
import pdfplumber
import os
import re

# Path to the source PDF
pdf_path = r'C:\meds_pipeline\data\0_raw\MEDICATION_PF.pdf'
# List to store extracted rows
dados = []

# Function to extract structured data from a text line within the PDF
def extract_data(linha):
    try:
         # Match the pattern for the 10-digit TISS code and up to 8-digit TUSS code
        match = re.match(r'^(\d{10})\s+(\d{0,8})\s+(.*)', linha)
        if not match:
            return None

        codigo_tiss = match.group(1).strip()
        codigo_tuss = match.group(2).strip()
        restante = match.group(3).strip()

        # Find the last numeric value (with commas) representing the price
        match_valor = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2,4})\s*(REAL)?$', restante)
        if match_valor:
            valor = match_valor.group(1).replace('.', '').replace(',', '.')
            cobranca = match_valor.group(2) if match_valor.group(2) else ''
            texto_antes_valor = restante[:match_valor.start()].rstrip()

            # Extract laboratory name (last word before the price)
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
    

# Open the PDF and iterate through each page to extract text lines

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[:288]:   # limit to the first 288 pages
        linhas = page.extract_text().split('\n')
        for linha in linhas:
            if linha.strip() and re.match(r'^\d{10}', linha):  # Consider only valid lines starting with a 10-digit code
                dados_linha = extract_data(linha)
                if dados_linha:
                    dados.append(dados_linha)

# Create a DataFrame from extracted data
colunas = ['codigo_tiss', 'codigo_tuss', 'produto', 'laboratorio', 'valor', 'cobranca']
df = pd.DataFrame(dados, columns=colunas)

df['valor'] = df['valor'].astype(float)

df.to_csv(r'C:\meds_pipeline\data\1_trusted\tabala_brasindice.csv',index=False)