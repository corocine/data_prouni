import pandas as pd
import sqlite3
from pathlib import Path
from utils import *


BASE_DIR = Path.cwd()
db_path = BASE_DIR / 'data' / "prouni.sqlite"

#  ----- table1 -------
conn_cursos = sqlite3.connect(db_path)
df_cursos = pd.read_sql_query('SELECT * FROM table1', conn_cursos)
conn_cursos.close()

# ---  data clean ---

df_cursos['grau'] = df_cursos['grau'].fillna('Não especificado')
df_cursos['grau'] = df_cursos['grau'].str.strip()

df_cursos['turno'] = df_cursos['turno'].fillna('Não especificado')
df_cursos['turno'] = df_cursos['turno'].str.strip()

df_cursos['mensalidade'] = df_cursos['mensalidade'].fillna('Não especificado')

df_cursos['curso_busca'] = df_cursos['curso_busca'].fillna('Não especificado')
df_cursos['curso_busca'] = df_cursos['curso_busca'].str.strip()

df_cursos['cidade_busca'] = df_cursos['cidade_busca'].fillna('Não especificado')
df_cursos['cidade_busca'] = df_cursos['cidade_busca'].str.strip()

df_cursos['uf_busca'] = df_cursos['uf_busca'].fillna('Não especificado')
df_cursos['uf_busca'] = df_cursos['uf_busca'].str.strip()
df_cursos['uf_busca'] = df_cursos['uf_busca'].str.upper()

df_cursos['campus_nome'] = df_cursos['campus_nome'].fillna('Não especificado')
df_cursos['campus_nome'] = df_cursos['campus_nome'].str.strip()

df_cursos['universidade_nome'] = df_cursos['universidade_nome'].fillna('Não especificado')
df_cursos['universidade_nome'] = df_cursos['universidade_nome'].str.strip()

scholarship_columns = [
    'bolsa_integral_cotas', 'bolsa_integral_ampla', 
    'bolsa_parcial_cotas', 'bolsa_parcial_ampla'
]
df_cursos[scholarship_columns] = df_cursos[scholarship_columns].fillna(0).astype(int)

duplicates = df_cursos.duplicated().sum()
if duplicates > 0:
    df_cursos = df_cursos.drop_duplicates()
    print(f"- {duplicates} linhas duplicadas foram removidas.")

# --- save data in a new archive ---
clean_db_path = BASE_DIR / 'data' / "clean_prouni.sqlite"
new_conn_table1 = sqlite3.connect(clean_db_path)
df_cursos.to_sql("cursos", new_conn_table1, if_exists='replace', index=False)
new_conn_table1.close()


#  ---- table 2 -----
conn_enderecos = sqlite3.connect(db_path)
df_enderecos = pd.read_sql_query('SELECT * FROM table2 ', conn_enderecos)

# --- data clean ---
df_enderecos['complemento'] = df_enderecos['complemento'].fillna('Não especificado')
df_enderecos['complemento'] = df_enderecos['complemento'].str.strip(' -')
df_enderecos['complemento'] = df_enderecos['complemento'].str.strip('- ')
df_enderecos['complemento'] = df_enderecos['complemento'].str.strip('S/n -')
df_enderecos['complemento'] = df_enderecos['complemento'].str.strip('º -')
df_enderecos['complemento'] = df_enderecos['complemento'].str.strip('')
df_enderecos['complemento'] = df_enderecos['complemento'].replace(['.', ' - - ', ' ', '°', '-','', 'S/n  -', 'S/N', 'S/n', 'n/d'], 'Não especificado' )
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace(' - - ', ' ')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??mpar', 'Ímpar')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??regon', 'Éregon')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??rea', 'Área')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??gua', 'Água')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??guas', 'Águas')
df_enderecos['complemento'] = df_enderecos['complemento'].str.replace('??rico', 'Érico')

df_enderecos['bairro'] = df_enderecos['bairro'].replace(['.', '°', '-', 'n/a', 'S/N', 'S/n', 'n/d'], 'Não especificado' )
df_enderecos['bairro'] = df_enderecos['bairro'].fillna('Não especificado')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??rea', 'Área')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??den', 'Éden')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??gua', 'Água')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??guas', 'Águas')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??tila', 'Átila')
df_enderecos['bairro'] = df_enderecos['bairro'].str.replace('??rvore', 'Árvore')
    
df_enderecos['municipio_limpo'] = df_enderecos['municipio'].str.lower()
df_enderecos['municipio_limpo'] = df_enderecos['municipio_limpo'].apply(remove_accents)
df_enderecos['municipio_limpo']= df_enderecos['municipio_limpo'].str.title()

df_enderecos['telefone'] = df_enderecos['telefone'].str.strip()
df_enderecos['telefone'] = df_enderecos['telefone'].replace(['','00', '°', '-', 'S/n -', 'S/N', 'S/n', 'n/d'], 'Não especificado' )
df_enderecos['telefone_limpo'] = df_enderecos['telefone'].apply(clean_phone)
df_enderecos['telefone_formatado'] = df_enderecos['telefone_limpo'].apply(format_phone)

df_enderecos['logradouro'] = df_enderecos['logradouro'].fillna('Não especificado')
df_enderecos['logradouro'] = df_enderecos['logradouro'].str.strip(' ,')


# --- save data in a new archive ---
clean_db_path = BASE_DIR / 'data' / "clean_prouni.sqlite"

new_conn_table2 = sqlite3.connect(clean_db_path)
df_enderecos.to_sql("enderecos", new_conn_table2, if_exists='replace', index=False)
new_conn_table2.close()
