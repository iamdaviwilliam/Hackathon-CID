import pandas as pd

df = pd.read_csv('data/postings.csv')

print(df.columns)

df['texto_completo_vaga'] = df['title'] + " " + df['description'] + " " + df['skills_desc'] 