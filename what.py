import requests
from bs4 import BeautifulSoup
import time
import re

# Função para fazer scraping na página inicial e obter links dos anúncios
def get_anuncio_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser')
        anuncios = soup.find_all('a', class_='job_listing-clickbox')  # Atualize a classe conforme necessário
        links_anuncios = [anuncio['href'] for anuncio in anuncios]
        return links_anuncios
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return []

# Função para fazer scraping em cada link de anúncio para encontrar links de chat
def get_chat_links(anuncio_url):
    try:
        response = requests.get(anuncio_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        chat_links = soup.find_all('a', class_='botoesChatAnunciante background-whats')
        chat_urls = [chat_link['href'] for chat_link in chat_links]
        return chat_urls
    except requests.RequestException as e:
        print(f"Erro ao acessar o anúncio {anuncio_url}: {e}")
        return []

# Função para extrair nome e telefone da URL do WhatsApp
def extract_name_and_phone(url):
    match = re.search(r'phone=(\d+)&text=oi%2C%20([^%]+)', url)
    if match:
        phone = match.group(1)
        name = match.group(2).replace('%20', ' ')
        return name, phone
    return None, None

# Função principal
def main():
    url = 'https://garotacomlocal.com/acompanhantes/sao-paulo-sp/'
    anuncio_links = get_anuncio_links(url)
    phones_seen = set()  # Conjunto para armazenar números de telefone já vistos

    for anuncio_link in anuncio_links:
        chat_urls = get_chat_links(anuncio_link)

        for chat_url in chat_urls:
            name, phone = extract_name_and_phone(chat_url)
            
            if name and phone not in phones_seen:
                print(f'Nome: {name}, Telefone: {phone}')
                phones_seen.add(phone)  # Adicionar telefone ao conjunto de números já vistos
        
        time.sleep(1)  # Adiciona um atraso de 1 segundo entre as requisições para evitar sobrecarregar o servidor

if __name__ == '__main__':
    main()
