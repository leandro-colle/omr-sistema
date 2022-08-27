# Sistema de reconhecimento óptico de partituras

Sistema OMR desenvolvido para trabalho de conclusão de curso. As ferramentas utilizadas foram Opencv, Tensorflow e MIDIUtil.

## Dependências

A versão do Python utilizada para o desenvolvimento do projeto foi a 3.6. A instalação do ambiente pode ser feita através do gerenciador de pacotes `anaconda`. O restante das dependências podem ser instaladas com o comando `pip install -r requirements.txt`

### Modelo semântico

A classificação dos símbolos musicais é feita através o modelo semântico treinado por rede neural. O modelo está disponível em: https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip e deve ser baixado e copiado para o diretório `/data` do projeto.

### Vocabulário semântico

Para conversão dos objetos classificados em significado de palavras, foi utilizado o vocabulário semântico disponível em: https://github.com/OMR-Research/tf-end-to-end, no diretório `Data/vocabulary_agnostic.txt`. Métodos do arquivo `ctc_utils.py` também foram utilizados como referência.

## Execução do sistema

`python3 main.py`