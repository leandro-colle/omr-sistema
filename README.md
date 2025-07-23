# Sistema de Reconhecimento Óptico de Partituras (OMR)

![Python](https://img.shields.io/badge/python-3.6-blue)
![License](https://img.shields.io/badge/license-mit-lightgrey)

> **Transforme partituras em áudio MIDI automaticamente usando visão computacional e redes neurais.**

O **Sistema de Reconhecimento Óptico de Partituras (OMR)** é uma solução desenvolvida para converter imagens de partituras musicais em arquivos de áudio MIDI, utilizando técnicas avançadas de visão computacional (OpenCV), redes neurais (TensorFlow) e manipulação MIDI (MIDIUtil). O projeto foi concebido como Trabalho de Conclusão de Curso, mas é ideal para músicos, pesquisadores e desenvolvedores interessados em digitalização e análise musical.

---

## Tabela de Conteúdos
- [Instalação e Dependências](#instalação-e-dependências)
- [Imagens e Datasets](#imagens-e-datasets)
- [Execução do Sistema](#execução-do-sistema)
- [Arquivos Gerados](#arquivos-gerados)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)
- [Contato](#contato)

---

## Instalação e Dependências

### Pré-requisitos
- Python 3.6 (recomenda-se uso de ambiente virtual ou Anaconda)
- Git

### Instalação

Clone o repositório e instale as dependências:

```bash
git clone git@github.com:leandro-colle/omr-sistema.git
cd omr-sistema
pip install -r requirements.txt
```

Principais dependências:
- OpenCV
- TensorFlow 1.1
- numpy
- protobuf
- MIDIUtil

### Modelos e Vocabulário

- Baixe o modelo semântico treinado: [Semantic-Model.zip](https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip) e extraia em `data/`.
- Baixe o vocabulário semântico: [vocabulary_agnostic.txt](https://github.com/OMR-Research/tf-end-to-end/blob/master/Data/vocabulary_agnostic.txt) e coloque em `data/` como `vocabulary_semantic.txt`.

---

## Imagens e Datasets

O sistema trabalha com imagens de partituras localizadas no diretório `/images`, organizadas em dois conjuntos principais:
- **primus-dataset**: imagens extraídas do repositório PRIMUS ([link](https://grfia.dlsi.ua.es/primus/)).
- **user-generated**: imagens criadas pelo usuário, por exemplo, via software Noteflight.

Para criar um novo dataset, inclua em `/images/<nome_dataset>`:
- Imagem de pauta (`.png`)
- Arquivo semântico (`.semantic`), seguindo o vocabulário de palavras adotado.

---

## Execução do Sistema

Execute o sistema informando o diretório do dataset de imagens:

```bash
python3 main.py <diretorio_dataset>
```

Exemplo:
```bash
python3 main.py images/primus-dataset
```

Caso o diretório não seja informado, o sistema solicitará o caminho.

---

## Arquivos Gerados

Durante a execução, o sistema gera automaticamente:
- **Imagem pré-processada** (`_processed.png`): resultado do alinhamento e binarização da pauta.
- **Arquivo de erros de classificação** (`.misclassified`): lista de símbolos classificados incorretamente, se houver.
- **Arquivo de áudio MIDI** (`.mid`): gerado quando a classificação da pauta atinge 100% de acerto.

Os arquivos de saída são salvos em `outputs/` e/ou no diretório das imagens processadas.

---

## Como Contribuir

Contribuições são muito bem-vindas! Para colaborar:

1. Faça um fork do projeto
2. Crie uma branch descritiva (`git checkout -b feature/nome-da-feature`)
3. Realize seus commits de forma clara e objetiva (`git commit -am 'Descrição da alteração'`)
4. Envie para seu fork (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request detalhando sua contribuição

Sugestões, correções e novas ideias são sempre incentivadas. Sinta-se à vontade para abrir issues para discussões ou dúvidas.

---

## Licença

Este projeto está licenciado sob os termos descritos no arquivo [LICENSE](./LICENSE) presente neste repositório.
