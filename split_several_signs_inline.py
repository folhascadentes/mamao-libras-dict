from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

texts = []


def split_text_in_lines(text, index):
    client = OpenAI()
    system = """
Separa o texto em múltiplas linhas quando detectar um padrão semelhante ao seguinte

<NOME DO SINAL> <(POSSIVEL NUMERACAO)> <(sinal usado em: ESTADOS)> <(Inglês: TRADUÇÃO)>

Exemplo #1:

AÇAI (1)  (sinal usado em: SP) (Inglês: Amazon açai fruit; small black fruit from a sort of coconut tree): S. m. Fruto de que se extrai uma polpa escura, muito apreciada para consumo. É um elemento precioso na alimentação dos habitantes da Amazônia, pois é muito rico em ferro. Ex.: o suco de açai tem um sabor delicioso. (Mãos em A, palmas para baixo, lado a lado. Balançá-las pelo pulso para cima e para baixo.)AÇAi (2) (sinal usado em: PA): Idem AÇAi (1). (Mãos em C, palmas para baixo, lado a lado, diante do abdômen. Movê-las ligeiramente para baixo, fechando-as em S, duas vezes.)acalentar

Resposta #1:

AÇAI (1)  (sinal usado em: SP) (Inglês: Amazon açai fruit; small black fruit from a sort of coconut tree): S. m. Fruto de que se extrai uma polpa escura, muito apreciada para consumo. É um elemento precioso na alimentação dos habitantes da Amazônia, pois é muito rico em ferro. Ex.: o suco de açai tem um sabor delicioso. (Mãos em A, palmas para baixo, lado a lado. Balançá-las pelo pulso para cima e para baixo.)
AÇAi (2) (sinal usado em: PA): Idem AÇAi (1). (Mãos em C, palmas para baixo, lado a lado, diante do abdômen. Movê-las ligeiramente para baixo, fechando-as em S, duas vezes.)acalentar

Faça o mesmo para o seguinte texto:
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
        top_p=1,
    )
    texts.append(response.choices[0].message.content)

    with open(f"tmp/{index}.txt", "w") as f_out:
        f_out.write(response.choices[0].message.content)


lines = []

with open("signs.out", "r") as f:
    for line in f.read().split("\n"):
        if line.count("(sina") > 1:
            lines.append(line)


with ThreadPoolExecutor(max_workers=10) as executor:
    for index, line in enumerate(lines):
        executor.submit(split_text_in_lines, line, index)


for text in texts:
    print(text)
