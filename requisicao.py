import requests
from bs4 import BeautifulSoup

# Defina a URL base para o Google Shopping
url = 'https://www.google.com/search'

# Defina a consulta de pesquisa
digitar = 'rtx 4060'

# Parâmetros da consulta
params = {
    'q': digitar,
    'tbm': 'shop'  # 'tbm=shop' indica que estamos procurando na aba de compras
}

# Envie a solicitação GET com os parâmetros de pesquisa
response = requests.get(url, params=params)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analise a resposta HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    produtos = soup.find_all('div', class_='sh-dgr__gr-auto sh-dgr__grid-result')
    print(produtos)
    for produto in produtos:
        nome = produto.find('div', class_='Lq5OHe eaGTj translate-content')
        if nome:
            
            print(nome.text)
        else:
            print('Não encontrado')
    # Imprima o título da página para verificar se a pesquisa foi bem-sucedida
    # print(soup.title.text)
else:
    print('A solicitação falhou com o status:', response.status_code)
