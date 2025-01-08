import pandas as pd

datasets = ['manually_annotated.csv', 'gpt_annotated.csv', 'llama_annotated.csv', 'gemini_annotated.csv', 'mistral_annotated.csv']

for df in datasets:
    dataset = pd.read_csv(df, index_col='Index')
    dataset.drop(columns=['Unnamed: 0'], inplace=True)
    dataset.to_csv(df)
