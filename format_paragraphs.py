from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor


def process_signs(signs_batch, batch_index, client):
    signs_to_process_txt = "\n".join(signs_batch)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": signs_to_process_txt,
            },
        ],
        temperature=0.0,
        top_p=1,
    )

    # Escreve a resposta em um arquivo JSON
    with open(f"json/{batch_index}.json", "w") as f_out:
        f_out.write(response.choices[0].message.content)


client = OpenAI()
system = """
Ao analisar as descrições fornecidas de sinais da Língua Brasileira de Sinais (Libras), estruture as informações em um formato JSON seguindo estas orientações detalhadas para cada campo:

1. "id": Deve conter o nome do sinal em Libras.
2. "region": Especifique as regiões geográficas onde o sinal é utilizado.
3. "parameters": Forneça uma descrição exclusivamente focada nos parâmetros físicos do sinal. Isso inclui a configuração da mão, a orientação da palma, movimentos e posições. Não inclua a definição ou tradução do sinal nesta seção.
4. "example": Inclua um exemplo de uso do sinal na comunicação.
5. "grammatical": Identifique a categoria gramatical do sinal.
6. "translation": Traduza o sinal para o inglês.
7. "cl": Indique se o sinal é um classificador (CL).
8. "etimologia": Forneça a etimologia do sinal, se disponível.

Por favor, garanta precisão e clareza nas descrições, aderindo estritamente às especificações para cada campo. 

O retorno esperado deve seguir o formato:

[
  {
    "id": "[Nome do Sinal]",
    "region": "[Regiões Geográficas]",
    "parameters": "[Descrição Detalhada dos Parâmetros Físicos do Sinal]",
    "example": "[Exemplo de Uso]",
    "grammatical": "[Categoria Gramatical]",
    "translation": "[Tradução para o Inglês]",
    "cl": "[Informação se é um classificador (CL)]",
    "etimologia": "[Etimologia do Sinal]"
  },
  ...
]

Segue a lista de sinais para análise:
"""
signs = []

file_path = "book.out"

if os.path.isfile(file_path):
    with open(file_path, "r") as f:
        signs = f.read().split("\n")

batch_size = 1

os.makedirs("json", exist_ok=True)

with ThreadPoolExecutor(max_workers=10) as executor:
    for index in range(0, len(signs), batch_size):
        json_file_path = f"json/{index}.json"

        if not os.path.isfile(json_file_path):
            executor.submit(
                process_signs, signs[index : index + batch_size], index, client
            )
