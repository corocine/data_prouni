import pandas as pd
import numpy as np
import unicodedata
import re
import numpy as np


def clean_phone(phone_column):
    """
    This function takes a value from the phone column, clears it and returns it,
    but now IGNORE cleaning if it finds the word "extension".
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
    """
    Improved formatting function to handle duplicate numbers and leading zeros.
    """
    if pd.isna(clean_phone_column):
        return np.nan

    phone = str(clean_phone_column)

    if 'ramal' in phone.lower():
        return phone

    if len(phone) == 11 and phone.startswith('0'):
        phone = phone[1:]
        
    if len(phone) == 11: return f"({phone[:2]}) {phone[2]} {phone[3:7]}-{phone[7:]}"
    if len(phone) == 10: return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    if len(phone) == 9: return f"{phone[0]} {phone[1:5]}-{phone[5:]}"
    if len(phone) == 8: return f"{phone[:4]}-{phone[4:]}"

    if len(phone) >= 19:
        
        half = len(phone) // 2
        num1 = phone[:half]
        num2 = phone[half:]
           
        if num1 == num2:
            return format_phone(num1)
        else:

            return f"{format_phone(num1)} / {format_phone(num2)}"
        
    return phone

def remove_accents(text):
    """
    Remove accents from words
    """
    # Normaliza a string para a forma 'NFKD' que separa as letras dos acentos
    nfkd_form = unicodedata.normalize('NFKD', str(text))
    # Mantém apenas os caracteres que não são de combinação (os acentos)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
