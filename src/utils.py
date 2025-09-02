import pandas as pd
import numpy as np
import unicodedata
import re
import numpy as np
import sqlite3
from pathlib import Path
import streamlit as st
import locale

def clean_phone(phone_column):
    """Clears and normalizes a phone number.

    This function takes a value from the phone column, removes characters
    non-numeric and returns it. Cleaning is skipped if the word "extension"
    is found.

    Args:
        phone_column (str or float): The value of the phone to clear.

    Returns:
        str: The clean phone number or the original string if it contains "extension".
             Returns 'Unspecified' if the input is null.
    """
    if pd.isna(phone_column):
        return 'Não especificado'

    phone_str = str(phone_column)
    
    if 'ramal' in phone_str.lower():
        return phone_str
    
    digits = re.sub(r'\D', '', phone_str)
    
    if 8 <= len(digits) <= 11:
        return digits
    elif 19 <= len(digits) <= 21:
        return digits
    else:
        return phone_str
    
def format_phone(clean_phone_column):
    """Formats a clean phone number to the Brazilian standard.

    Args:
        clean_phone_column (str): The clean phone number (digits only).

    Returns:
        str: The formatted phone number (ex: (XX) Y XXXX-XXXX) or
             'Not specified' if the number is invalid.
    """
    if pd.isna(clean_phone_column):
        return np.nan

    phone = str(clean_phone_column)

    if 'ramal' in phone.lower():
        return phone
    
    if not phone.isdigit():
        return 'Não especificado'
    
    if len(phone) < 8 or len(phone) > 11:
        return 'Não especificado'

    if len(phone) == 11 and phone.startswith('0'):
        phone = phone[1:]
        
    if len(phone) == 11: return f"({phone[:2]}) {phone[2]} {phone[3:7]}-{phone[7:]}"
    if len(phone) == 10: return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    if len(phone) == 9: return f"{phone[0]} {phone[1:5]}-{phone[5:]}"
    if len(phone) == 8: return f"{phone[:4]}-{phone[4:]}"

    return phone

def remove_accents(text):
    """Removes accents from a text string.

    Args:
        text (str): The string to remove accents from.

    Returns:
        str: The string without accents.
    """
    # Normaliza a string para a forma 'NFKD' que separa as letras dos acentos
    nfkd_form = unicodedata.normalize('NFKD', str(text))
    # Mantém apenas os caracteres que não são de combinação (os acentos)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
def load_data_with_join(db_path, filters=None):
    """Loads and joins data from tables, applying dynamic filters.

    This function executes an SQL query to join the `courses` and
    `addresses` and applies filters based on the provided dictionary.

    Args:
        db_path (str or Path): The path to the SQLite database.
        filters (dict, optional): A dictionary of filters to apply
                                  in the consultation. The keys are the names of the
                                  columns and the values ​​are the values ​​to
                                  filter. Defaults to None.

    Returns:
        pd.DataFrame: A Pandas DataFrame with the filtered data.
    
    Raises:
        ValueError: If an error occurs while loading the data.
    """
    base_query = """
    SELECT 
        c.curso_busca AS curso,
        c.grau AS nível,
        c.turno AS período,
        c.mensalidade,
        c.universidade_nome AS universidade,
        c.campus_nome,
        c.bolsa_integral_cotas,
        c.nota_integral_cotas AS nota_corte_integral_cotas,
        c.bolsa_integral_ampla AS bolsa_integral,
        c.nota_integral_ampla AS nota_corte_integral,
        c.bolsa_parcial_cotas,
        c.nota_parcial_cotas AS nota_parcial_cotas,
        c.bolsa_parcial_ampla AS bolsa_parcial,
        c.nota_parcial_ampla AS nota_parcial,
        e.municipio_limpo AS município,
        e.uf AS estado,
        e.telefone_formatado AS telefone
    FROM 
        cursos AS c
    INNER JOIN 
        enderecos AS e ON c.campus_id = e.id
    """
    
    conn = None
    params = []
    where_clauses = []

    if filters:
        for column, value in filters.items():
            if value:
                if isinstance(value, list):
                    placeholders = ','.join('?' for _ in value)
                    where_clauses.append(f"TRIM({column}) IN ({placeholders})")
                    params.extend(value)
                else:
                    where_clauses.append(f"TRIM({column}) LIKE ?")
                    params.append(f'%{value}%')

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    try:
        conn = sqlite3.connect(db_path)
        df_filtered = pd.read_sql_query(base_query, conn, params=params)
        return df_filtered
    except Exception as e:
        raise ValueError(f"Error loading data from {db_path}: {e}")
    finally:
        if conn:
            conn.close()
            
@st.cache_data
def get_unique_values(db_path, table_name, column_name):
    """Search for unique values ​​from a database column in a cached manner.

    Args:
        db_path (str or Path): The path to the SQLite database.
        table_name (str): The name of the table.
        column_name (str): The name of the column.

    Returns:
        list: A list of unique values ​​from the specified column.
    """
    if not Path(db_path).exists():
        return []
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        query = f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL ORDER BY {column_name};"
        df = pd.read_sql_query(query, conn)
        return df[column_name].tolist()
    except Exception as e:
        st.error(f"Erro ao buscar valores únicos para {column_name}: {e}")
        return []
    finally:
        if conn:
            conn.close()
            
def format_to_brazilian_currency(number):
    """Formats a number for the Brazilian currency standard (BRL).

    Args:
        number (float or int): The number to be formatted.

    Returns:
        str: The number formatted as currency (ex: R$ 1,234.56) or "R$ -" if
             the entry is null.
    """
    if pd.isna(number):
        return "R$ -"
    try:
        # Linux/MacOS
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
    except locale.Error:
        # Windows
        locale.setlocale(locale.LC_MONETARY, 'Portuguese_Brazil.1252')

    return locale.currency(number, grouping=True)

def replace_comma_with_dot(number):
    """Formats a number with thousand-dot separators.

    Args:
        number (int or float): The number to be formatted.

    Returns:
        str: The number formatted with dots as thousands separators
             (e.g. 1,234).
    """
    return f"{number:,.0f}".replace(",", ".")
