# Copa Transparente

Objetivos:

* Disponibilizar um grafo rico dos meta-dados da base de dados dos gastos com a Copa (tabelas, pks e fks).
* Disponibilizar um grafo fico dos dados dos gastos com a Copa.

## Processamento de Meta Dados

1. Download de uma base mensal

```sh
python download_dados_copa.py
```

2. Extraindo todos arquivos

```sh
python extrai_banco.py
```

3. Le meta dados

```sh
python le_meta_dados.py
```

4. Gera modelo visual

```sh
python analise_meta.py > relacionamentos.dot
dot -T png relacionamentos.dot -o relacionamentos.png
```
