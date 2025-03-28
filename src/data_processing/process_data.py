import pdfplumber
import csv
import zipfile
import os
from tabulate import tabulate

# Caminhos dos arquivos
pdf_path = "../downloads_pdf/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_filename = "tabela_completa.csv"
zip_filename = "Teste_Brenda.zip"

# substituicao das colunas OD e AMB 
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}


with pdfplumber.open(pdf_path) as pdf:
    with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        full_table = []

        for page_num, page in enumerate(pdf.pages):
            print(f"Processando página {page_num + 1}...")

            table = page.extract_table()

            if table:
                # Separação das tabelas
                full_table.append([f"Tabela da página {page_num + 1}"])
                full_table.append([""] * len(table[0]))  

                # Organiza as linhas
                for row in table:
                    cleaned_row = [
                        substituicoes.get(cell.strip(), cell.strip()).replace("\n", " ") if cell else "" 
                        for cell in row
                    ]
                    full_table.append(cleaned_row)

                full_table.append([""] * len(table[0]))  

            else:
                print(f"Nenhuma tabela encontrada na página {page_num + 1}.")

        # formatação das tabelas
        formatted_table = tabulate(full_table, headers="firstrow", tablefmt="csv")

        csv_file.write(formatted_table.replace(",", ";"))

    print(f"Todas as tabelas foram salvas no arquivo {csv_filename}")

# Compactação em um arquivo ZIP 
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename, os.path.basename(csv_filename))

print(f"Arquivo {zip_filename} criado com sucesso!")

# Remove o csv após compactação
os.remove(csv_filename)
print(f"Arquivo {csv_filename} removido após compactação.")
