# mamao-libras-dict

Project to extract information of Libras signs from "Dicionário da Língua de Sinais do Brasil: a Libras em Suas Mãos"

## Depndencies

- Python 3.8
- Amazon SDK Environment Variables
- OpenAI Environment Variables

## Workflow

- main.py
- merge_texts.py (and manually clean and analyse the results)
- clean_merge_text.py
- manual step to clean data output by clean_merge_text.py
- format_paragraphs.py
- extract_parameters.py

## Example of output of each pipeline

### Book

The PDF containing the digitalized book of reference

Not avaiable in this repository due to copy rights

### Images

The images of each page of the book

### Raw texts

The raw texts extracted from the images using OCR

```text
45
A
Dicionário da Língua de Sinais do Brasil: A Libras em suas mãos
Femando C. Capovilla, Walkiria D. Raphael, Janice G. Temoteo, e Antonielle C. Martins
A, a: S. m. Primeira letra do alfabeto do Português antes do "b", e
A
primeira vogal antes do "e". Ex.: A palavra "alegria" começa com a letra
"a". num. e adj. m. e f. o primeiro item, numa série ou enumeração
indicada pelas letras do alfabeto. Ex.: o item "a" do contrato descreve
direitos e deveres. (Fonética) o fonema /a/ é uma vogal média, baixa, e
oral. (Mão vertical fechada, palma para frente, polegar tocando a lateral
do indicador.)
À DIREITA (sinal usado em: CE,
DF, PR, RS, SC, SP) (Inglês: to
the right): loc. adv. lugar Para a
direita, para o lado direito. Ex.:
Se você virar à direita chegará à
escola. (Mão em B horizontal, palma para frente, dedos inclinados para a direita. Movê-la ligeiramente para a direita.)
to
À ESQUERDA (sinal usado em:
```

### Formatted texts

The raw texts formatted in a more readable way

```text
A, a: S. m. Primeira letra do alfabeto do Português antes do "b", e a primeira vogal antes do "e". Ex.: A palavra "alegria" começa com a letra "a". num. e adj. m. e f. o primeiro item, numa série ou enumeração indicada pelas letras do alfabeto. Ex.: o item "a" do contrato descreve direitos e deveres. (Fonética) o fonema /a/ é uma vogal média, baixa, e oral. (Mão vertical fechada, palma para frente, polegar tocando a lateral do indicador.)

À DIREITA (sinal usado em: CE, DF, PR, RS, SC, SP) (Inglês: to the right): loc. adv. lugar Para a direita, para o lado direito. Ex.: Se você virar à direita chegará à escola. (Mão em B horizontal, palma para frente, dedos inclinados para a direita. Movê-la ligeiramente para a direita.)
```

### Observações

Sinais como o seguinte, que não possuem dados dos parametros, como CM, PA, MOV e ORI, são ignorados nessa analise inicial

```
A FIM DE (3) : Mover a cabeça levemente para frente e piscar um dos olhos.

[
  {
    "head": {
      "orientation": "front_down",
      "winky": true
    }
  }
]

```
