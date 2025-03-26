import requests
import os
from bs4 import BeautifulSoup
import zipfile

# Pasta onde os PDFs serão salvos
download_folder = 'downloads_pdf'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscando os links dos PDFs
    pdf_links = [link['href'] for link in soup.find_all('a', href=True) 
                 if ('Anexo_I' in link['href'] or 'Anexo_II' in link['href']) and '.pdf' in link['href']]

    print(pdf_links)

else:
    print("Erro ao acessar o site:", response.status_code)

# Lista para armazenar os caminhos dos arquivos PDF
pdf_files = []

# Baixar e salvar os PDFs
for link in pdf_links:
    response = requests.get(link)  

    if response.status_code == 200:
        # Pega a última parte da URL para nomear o arquivo
        filename = link.split("/")[-1]
        file_path = os.path.join(download_folder, filename)  # Caminho completo

        # Salva na pasta "downloads_pdf"
        with open(file_path, 'wb') as file:
            file.write(response.content)  
        
        # Adiciona o caminho do arquivo à lista pdf_files
        pdf_files.append(file_path)

        print(f"Arquivo {filename} baixado com sucesso em {file_path}!")
    else:
        print(f"Falha ao baixar {link}")

# Compacta os pdfs em um arquivo zip
zip_filename = os.path.join(download_folder, 'arquivos_rol.zip')

with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for pdf_file in pdf_files:
        zipf.write(pdf_file, os.path.basename(pdf_file))

print(f"Arquivos compactados com sucesso em {zip_filename}!")
