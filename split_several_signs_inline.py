from openai import OpenAI


def split_text_in_lines(text):
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
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        temperature=0.0,
        top_p=1,
    )

    return response.choices[0].message.content


count = 0

with open("signs.out", "r") as f:
    lines = f.read().split("\n")
    processed_lines = []
    for line in lines:
        if line.count("(sina") < 2:
            print(line)
        else:
            count += line.count("(sina") - 1
            print(split_text_in_lines(line))


print(count)
