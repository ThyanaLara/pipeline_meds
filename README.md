# Medication Data Cleaning

Extracting and standardizing medication data from unstructured PDF sources

## Overview
This project was born from a real challenge I faced at work.
I used to work with datasets where the same product appeared under multiple different codes and descriptions, making it almost impossible to perform consistent analysis.

A key issue was that the dosage (in mg/ml) — crucial to distinguish product variations — was often embedded within unstructured text fields or formatted inconsistently across systems.
So I decided to build a custom Python pipeline that could:

Extract medication information from a PDF table (in this case, BRASÍNDICE – a public medication reference);

Identify and clean product names;

Detect and normalize the dosage amount (mg/ml/g);

Combine both into a single standardized identifier that allows linking inconsistent records referring to the same medication.

This solution made it possible to analyze, group, and compare non-standardized data, which is common in healthcare and other industries that deal with product catalogs.

## Project
- Convert unstructured PDF data into an analytical dataset.
- Extract medication name, dosage, and value in a consistent format.
- Handle text variations, spacing issues, and mixed units (mg, ml, g).
- Enable future integration of distinct codes that refer to the same product.
- Create a replicable pipeline that can be adapted to other product types (not only medications).

