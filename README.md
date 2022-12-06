# Sistema de reconhecimento óptico de partituras

Sistema OMR desenvolvido para trabalho de conclusão de curso. As ferramentas utilizadas foram Opencv, Tensorflow e MIDIUtil.

## Dependências

A versão do Python utilizada para o desenvolvimento do projeto foi a 3.6. A instalação do ambiente pode ser feita através do gerenciador de pacotes `anaconda`. O restante das dependências podem ser instaladas com o comando `pip install -r requirements.txt`

### Modelo semântico

A classificação dos símbolos musicais é feita através o modelo semântico treinado por rede neural. O modelo está disponível em: https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip e deve ser baixado e copiado para o diretório `/data` do projeto.

### Vocabulário semântico

Para conversão dos objetos classificados em significado de palavras, foi utilizado o vocabulário semântico disponível em: https://github.com/OMR-Research/tf-end-to-end, no diretório `Data/vocabulary_agnostic.txt`. Métodos do arquivo `ctc_utils.py` também foram utilizados como referência.

## Imagens

As imagens utilizadas estão no diretório `/images`. Nesse diretório existem 2 tipos de imagens utilizadas. O diretório `primus-dataset` armazena as imagens extraídas do repositório de imagens PRIMUS (https://grfia.dlsi.ua.es/primus/). O diretório `user-generate` possui as imagens próprias geradas através do software Noteflight.

Para gerar um novo dataset, é preciso que existam os seguintes arquivos dentro do `/images/<nome_dataset>`:

- Imagem de pauta (`.png`)
- Arquivo semântico (`.semantic`), seguindo as regras do vocabulário de palavras

Ao executar o sistema, serão gerados os seguintes arquivos:

- Imagem pré-processada (`_processed.png`)
- Erros de classificação (`.misclassified`), caso houver
- Arquivo de audio (`.mid`), caso a etapa de classificação atinja 100% na classificação da pauta

## Execução do sistema

`python3 main.py <diretorio_dataset>`
