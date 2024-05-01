import requests
import pandas as pd

def scraping_request(url):
    headers = {
    'User-Agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 ,(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        df = pd.read_html(response.content, encoding='utf-8')[0]
    else:
        raise ValueError('Erro ao obter dados da URL.')
    
    return df

def float_transformer(df, cols):  # Função com o intuito de transformar as colunas para float
    for col in cols:
        df[col] = df[col].str.replace(',', '.').str.replace('%', '').str.replace('N/D', '0').str.replace('R$', '').astype(float)
    return df