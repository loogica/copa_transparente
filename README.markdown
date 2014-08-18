# Copa Transparente

O projeto `copa transparente` é uma aplicação Livre, feita para Python 3.3 (ou superior)
que:

* Faz o download de um arquivo de base de dados do projeto copa transparente e interpreta os dados.
* Permite consultas de dados, schema, lista de tabelas e outras coisas.

## Download de uma base de dados

```sh
python download.py timestamp(YYYYMMDD)
```

Exemplo - Download base 29/07/2014:

```sh
python download.py 20140729
```

## Le informações da base

```sh
$ python extrai.py -a
usage: extrai.py [-a] [-l] [-d DETALHE] [-c CONSULTA] [-g]

Extrai informação dos dados

optional arguments:
  -a, --ajuda           Exibe ajuda
  -l, --lista           Lista tabelas
  -d DETALHE, --detalhe DETALHE
                        Descrição de uma tabela
  -c CONSULTA, --consulta CONSULTA
                        Consulta dados de uma tabela
  -g, --dotlang         Gerar saída dotlang para gerar imagem
```

Com esse script é possível listar as tabelas disponíveis, ver a descrição dos campos, consultar os dados e gerar uma saída na linguagem
dotlang para que seja gerado uma imagem das tabelas e relacionamentos.

Para gerar a imagem do modelo de dados:

```sh
$ python extrai.py -g > relacionamentos.dot
$ dot -T png relacionamentos.dot -o relacionamentos.png
````
