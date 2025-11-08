# Medication Data Cleaning

Extracting and standardizing medication data from unstructured PDF sources

## Overview
[EN]This project was born from a real challenge I faced at work.
I used to work with datasets where the same product appeared under multiple different codes and descriptions, making it almost impossible to perform consistent analysis.

A key issue was that the dosage (in mg/ml) — crucial to distinguish product variations — was often embedded within unstructured text fields or formatted inconsistently across systems.
So I decided to build a custom Python pipeline that could:
   - Extract medication information from a PDF table;
   - Identify and clean product names;
   - Detect and normalize the dosage amount (mg/ml/g);
   - Combine both into a single standardized identifier that allows linking inconsistent records referring to the same medication.

This solution made it possible to analyze, group, and compare non-standardized data, which is common in healthcare and other industries that deal with product catalogs.

[PT] Este projeto surgiu de uma necessidade real que enfrentei no dia a dia de trabalho.
Eu costumava trabalhar com bases de dados onde o mesmo produto aparecia com vários códigos e descrições diferentes, o que tornava quase impossível realizar análises consistentes e identificar corretamente produtos iguais.

Um dos principais desafios era que a dosagem (em mg/ml) — que é primordial para diferenciar variações do produtos — estava frequentemente inserida em campos de texto não estruturados e sem formatação padronizada.

Por exemplo: havia descrições contendo apenas a dosagem em miligramas (50 mg), enquanto outras incluíam a concentração e o volume (10 mg/ml 5 ml) para o mesmo produto.
Com o objetivo de solucionar esse problema e tornar as análises mais assertivas, desenvolvi este pipeline de padronização, capaz de extrair o nome e a dosagem corretos dos medicamentos e unificar as informações em uma base confiável para análise.


## Project
- Convert unstructured PDF data into an analytical dataset.
- Extract medication name, dosage, and value in a consistent format.
- Handle text variations, spacing issues, and mixed units (mg, ml, g).
- Enable future integration of distinct codes that refer to the same product.
- Create a replicable pipeline that can be adapted to other product types (not only medications).

