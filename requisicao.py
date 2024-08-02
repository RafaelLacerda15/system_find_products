import requests
from bs4 import BeautifulSoup
from banco_dados import bd



class principal:
    def __init__(self, usuario):
        super().__init__()

        # Defina a URL base para o Google Shopping
        self.url = f'https://www.google.com/search?q={usuario}&tbm=shop'
        self.url_modificado = self.url.replace(" ", "+")
        # Cabeçalhos HTTP para simular um navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        

    def inicio(self):
        self.dados = bd()
        self.dados.create_table(table='resultados')
        
        resultado = []
        # Envie a solicitação GET para a URL
        response = requests.get(self.url_modificado, headers=self.headers)
        # Verifique se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Analise a resposta HTML com BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontre todos os elementos de resultado
            element_page = soup.find_all('div', class_='sh-dgr__content')
            contador = 0
            for x in element_page:
                # nome produto
                nome = x.find('div', class_='EI11Pd')
                # preço produto
                preco = x.find('span', class_='a8Pemb OFFNJ')
                # url produto
                link = x.find('div', class_='mnIHsc')
                href_a = link.find('a')
                href = href_a.get('href')
                # nome site produto
                site = x.find('div', class_='aULzUe IuHnof')
                
                # Verifique se as tags e classes foram encontradas
                if nome and preco and href_a:
                    # nome produto
                    nome = nome.text
                    # preço produto
                    preco = preco.text
                    # url produto modificado
                    href_modificado = f'https://www.google.com{href}'
                    # nome site produto
                    site_certo = site.text
                    
                    contador += 1
                    resultado.append((nome, preco, href_modificado, site_certo))
                    
                    self.dados.inserir_table(nome, preco, href_modificado, site_certo)

                    # print(contador, nome)
                    # print(site_certo)
                    # print(href_modificado)
                    # print(preco, "\n")
                else:
                    print("Alguma informação não foi encontrada.")
            return resultado
        else:
            print(f'A solicitação falhou com o status: {response.status_code}')

# bot = principal(usuario='rtx 4060')
# bot.inicio()