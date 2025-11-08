import pandas as pd
import os
import re

df = pd.read_csv(r'\meds_pipeline\data\1_trusted\database_brasindice.csv')

# Função para extrair a primeira palavra
def extrair_primeira_palavra(descricao):
    if pd.isna(descricao):  # Verificar valores nulos
        return descricao
    palavras = descricao.split()  # Dividir a descrição em palavras
    return palavras[0]  # Retornar apenas a primeira palavra

df['produto_limpo'] = df['produto'].apply(extrair_primeira_palavra)

# Função para extrair a mg ou ml 
def extrair_mg_total(descricao):
   descricao = str(descricao).lower()
   # Padronizações
   descricao = descricao.replace("miligrama", "mg").replace("miligramas", "mg").replace('mcg', 'mg')
   descricao = descricao.replace("mililitro", "ml").replace("mililitros", "ml")
   descricao = descricao.replace("grama", "g").replace("gramas", "g")

   # Corrigir decimais quebrados: "38 5 mg" → "38.5 mg", "2 5 ml" → "2.5 ml"
   # Essa regex trata qualquer número + espaço + número curto + mg/ml/g
   descricao = re.sub(r'(\d+)\s+(\d{1,2})\s*(mg|ml|g)', r'\1.\2 \3', descricao)
   # Corrigir milhar quebrado: "1 000 mg" → "1000 mg" (somente se for 3 dígitos após)
   descricao = re.sub(r'(?<!\d)(\d{1,2})\s+(\d{3})\s*mg', r'\1\2 mg', descricao)
   # Casos mg/ml: "X mg/ml Y ml" → calcular mg total
   padrao_mg_ml = re.search(r'(\d+(?:[\.,]\d+)?)\s*mg\s*(?:\/|\s*)ml.*?(\d+(?:[\.,]\d+)?)\s*ml', descricao)
   if padrao_mg_ml:
       mg_por_ml = float(padrao_mg_ml.group(1).replace(',', '.'))
       ml_total = float(padrao_mg_ml.group(2).replace(',', '.'))
       return round(mg_por_ml * ml_total, 2)
   # Casos com gramas → mg
   valores_g = re.findall(r'(\d+(?:[\.,]\d+)?)\s*g', descricao)
   if valores_g:
       valor_g = float(valores_g[-1].replace(',', '.'))
       return round(valor_g * 1000, 2)
   # Regra final: pegar o primeiro número antes de "mg"
   texto_antes_de_mg = descricao.split("mg")[0]
   numeros = re.findall(r'\d+(?:[\.,]\d+)?', texto_antes_de_mg)
   if numeros:
       return round(float(numeros[0].replace(',', '.')), 2)
   return None

df['mg_por_frasco'] = df['produto'].apply(extrair_mg_total)

# Nova coluna juntando o nome do produto com a quantidade mg ou ml
def juntar_colunas_prod_mg(row):
    descricao = row['produto_limpo']
    mg = row['mg_por_frasco']
 
    if pd.notna(mg):
         # Se for um número inteiro, mostra sem decimal
        if mg == int(mg):
            mg_formatado = int(mg)
        else:
            mg_formatado = round(mg, 2)  # ou 1 casa decimal se preferir
        return f"{descricao} {mg_formatado}mg"
    else:
        return descricao
    
df['produto_tratado'] = df.apply(juntar_colunas_prod_mg, axis=1)

colunas = ['codigo_tuss', 'produto', 'produto_tratado','laboratorio', 'valor']
df = df[colunas]

df.to_csv(r'\meds_pipeline\data\2_refined\medication_data_final.csv',index=False)