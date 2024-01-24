# mamao-libras-dict

Project to extract information of Libras signs from "Dicionário da Língua de Sinais do Brasil: a Libras em Suas Mãos"

## Depndencies

- Python 3.8
- Amazon SDK Environment Variables
- OpenAI Environment Variables


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

### JSON

The raw texts formatted in a JSON file for programatic use

```json
{
    "A, a": "Primeira letra do alfabeto do Português antes do 'b', e a primeira vogal antes do 'e'. Ex.: A palavra 'alegria' começa com a letra 'a'. O fonema /a/ é uma vogal média, baixa, e oral. (Mão vertical fechada, palma para frente, polegar tocando a lateral do indicador.)",
    "À DIREITA": "Lugar para a direita, para o lado direito. Ex.: Se você virar à direita chegará à escola. (Mão em B horizontal, palma para frente, dedos inclinados para a direita. Movê-la ligeiramente para a direita.)",
    "À ESQUERDA": "Lugar para a esquerda, para o lado esquerdo. Ex.: Virando à esquerda, você chegará mais depressa à sua casa. (Mão em B horizontal, palma para trás. Movê-la ligeiramente para a esquerda.)",
    "À EXCEÇÃO DE": "Exceto. Excetuado. Salvo. Menos. Afora. Ex.: Todos entraram à exceção dos retardatários. (Fazer este sinal MENOS (exceto): Mão esquerda horizontal aberta, palma para a direita; mão direita em 1, palma para baixo, indicador para frente. Passar a lateral do indicador direito para baixo sobre a palma esquerda.)",
    "A FIM DE (1)": "Indica desejo de, inclinação por, ou interesse em possuir algo; ou desejo e interesse em conhecer e namorar alguém. Ex.: Ele está a fim daquele carro há meses. Ex.: Estou a fim daquela garota. (Mão fechada, palma para baixo, diante da boca. Distender o dedo mínimo, várias vezes, com expressão facial de contentamento.)",
    "A FIM DE (2)": "Idem A FIM DE (1). (Fazer este sinal VONTADE: Mão em 1, passar a ponta do indicador para baixo sobre o pescoço, duas vezes. Em seguida, fazer este sinal FICAR: Mão em I com polegar na lateral, palma para a esquerda. Unha do polegar tocando abaixo do lábio inferior. Finalmente, fazer este sinal VOCÊ: Mão em 1 horizontal, palma para a esquerda. Apontar a outra pessoa com quem se está falando.)"
}
```