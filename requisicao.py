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
            element_page = soup.find_all('div', class_='sh-pr__product-results-grid sh-pr__product-results')
            contador = 0
            for x in element_page:
                nome = x.find('div', class_='EI11Pd')
                preco = x.find('span', class_='a8Pemb OFFNJ')
                img = x.find('div', class_='FM6uVc')
                link = x.find('div', class_='mnIHsc')
                href = link.get('href')
                print(href)
                # Verifique se as tags e classes foram encontradas
                if nome and preco:
                    nome = nome.text
                    preco = preco.text
                    
                    contador += 1
                    resultado.append((nome,preco))
                    
                    # self.dados.inserir_table(nome, preco)

                    # print(contador, nome)
                    # print(preco, "\n")
                else:
                    print("Alguma informação não foi encontrada.")
            return resultado
        else:
            print(f'A solicitação falhou com o status: {response.status_code}')

bot = principal(usuario='rtx 4060')
bot.inicio()