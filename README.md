# Sistema de reconhecimento óptico de partituras

Sistema OMR desenvolvido para trabalho de conclusão de curso. As ferramentas utilizadas foram Opencv, Tensorflow e MIDIUtil.

## Dependências

A versão do Python utilizada para o desenvolvimento do projeto foi 3.6. Instalação feita através do ambiente conda. O restante das dependências podem ser instaladas com o comando `pip install -r requirements.txt`

### Modelo semântico

A classificação dos símbolos musicais é feita através o modelo semântico treinado por uma rede neural. O modelo também está disponível em: https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip

### Vocabulário semântico

Para conversão dos objetos classificados em significado de palavras, foi utilizado o vocabulário semântico (`Data/vocabulary_agnostic.txt`) disponível em: https://github.com/OMR-Research/tf-end-to-end, além de métodos do arquivo `ctc_utils.py` como referência.

## Execução do sistema

`python3 main.py`