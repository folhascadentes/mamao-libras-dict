from openai import OpenAI

system = """
Ao analisar as descrições fornecidas de sinais da Língua Brasileira de Sinais (Libras), estruture as informações em um formato JSON seguindo estas orientações detalhadas para cada campo:

1. "id": Deve conter o nome do sinal em Libras.
2. "region": Especifique as regiões geográficas onde o sinal é utilizado.
3. "parameters": Forneça uma descrição exclusivamente focada nos parâmetros físicos do sinal. Isso inclui a configuração da mão, a orientação da palma, movimentos e posições. Não inclua a definição ou tradução do sinal nesta seção.
4. "example": Inclua um exemplo de uso do sinal na comunicação.
5. "grammatical": Identifique a categoria gramatical do sinal.
6. "translation": Traduza o sinal para o inglês.

Por favor, garanta precisão e clareza nas descrições, aderindo estritamente às especificações para cada campo. 

O retorno esperado deve seguir o formato:

[
  {
    "id": "[Nome do Sinal]",
    "region": "[Regiões Geográficas]",
    "parameters": "[Descrição Detalhada dos Parâmetros Físicos do Sinal]",
    "example": "[Exemplo de Uso]",
    "grammatical": "[Categoria Gramatical]",
    "translation": "[Tradução para o Inglês]"
  },
  ...
]

Segue a lista de sinais para análise:
"""

client = OpenAI()

with open("book_one.out", "r") as f:
    signs = f.read().split("\n")
    jump = 5

    for index in range(0, len(signs), jump):
        signs_to_process = signs[index : index + jump]
        signs_to_process_txt = "\n".join(signs_to_process)

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

        with open(f"json/{index}.json", "w") as f_out:
            f_out.write(response.choices[0].message.content)
