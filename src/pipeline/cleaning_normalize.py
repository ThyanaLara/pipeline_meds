"""
Script: cleaning_normalize.py
Author: Thyana Lara
Description: Cleans and normalizes product descriptions and dosage information from the extracted dataset.
"""
import pandas as pd
import os
import re

# Load the previously extracted dataset
df = pd.read_csv(r'\meds_pipeline\data\1_trusted\database_brasindice.csv')

# -----------------------------
# Function 1 — Extract the first word from the product name
# -----------------------------
def extract_first_word(description):
    if pd.isna(description):  # handle null values
        return description
    palavras = description.split()  
    return palavras[0]  

df['produto_limpo'] = df['produto'].apply(extract_first_word)

# -----------------------------
# Function 2 — Extract and normalize dosage (mg/ml/g)
# -----------------------------
def extract_total_mg(description):
   description = str(description).lower()
    # Normalize unit variations
   description = description.replace("miligrama", "mg").replace("miligramas", "mg").replace('mcg', 'mg')
   description = description.replace("mililitro", "ml").replace("mililitros", "ml")
   description = description.replace("grama", "g").replace("gramas", "g")

   # Fix broken decimals (e.g., "38 5 mg" → "38.5 mg", "2 5 ml" → "2.5 ml")
   description = re.sub(r'(\d+)\s+(\d{1,2})\s*(mg|ml|g)', r'\1.\2 \3', description)
   # Fix thousand separators (e.g., "1 000 mg" → "1000 mg")
   description = re.sub(r'(?<!\d)(\d{1,2})\s+(\d{3})\s*mg', r'\1\2 mg', description)
   # Handle "mg/ml" patterns (e.g., "X mg/ml Y ml" → total mg = X * Y)
   padrao_mg_ml = re.search(r'(\d+(?:[\.,]\d+)?)\s*mg\s*(?:\/|\s*)ml.*?(\d+(?:[\.,]\d+)?)\s*ml', description)
   if padrao_mg_ml:
       mg_por_ml = float(padrao_mg_ml.group(1).replace(',', '.'))
       ml_total = float(padrao_mg_ml.group(2).replace(',', '.'))
       return round(mg_por_ml * ml_total, 2)
   # Handle grams → convert to mg
   valores_g = re.findall(r'(\d+(?:[\.,]\d+)?)\s*g', description)
   if valores_g:
       valor_g = float(valores_g[-1].replace(',', '.'))
       return round(valor_g * 1000, 2)
   # Fallback: take the last number before 'mg'
   texto_antes_de_mg = description.split("mg")[0]
   numeros = re.findall(r'\d+(?:[\.,]\d+)?', texto_antes_de_mg)
   if numeros:
       return round(float(numeros[0].replace(',', '.')), 2)
   return None

df['mg_por_frasco'] = df['produto'].apply(extract_total_mg)

# -----------------------------
# Function 3 — Combine product name and dosage
# -----------------------------
def combine_product_mg(row):
    description = row['produto_limpo']
    mg = row['mg_por_frasco']
 
    if pd.notna(mg):
         # Format mg without unnecessary decimals
        if mg == int(mg):
            mg_formatado = int(mg)
        else:
            mg_formatado = round(mg, 2)  
        return f"{description} {mg_formatado}mg"
    else:
        return description
    
df['produto_tratado'] = df.apply(combine_product_mg, axis=1)

colunas = ['codigo_tuss', 'produto', 'produto_tratado','laboratorio', 'valor']
df = df[colunas]

df.to_csv(r'\meds_pipeline\data\2_refined\medication_data_final.csv',index=False)