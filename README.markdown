# Copa Transparente

Objetivos:

* Disponibilizar um grafo rico dos meta-dados da base de dados dos gastos com a Copa (tabelas, pks e fks).
* Disponibilizar um grafo fico dos dados dos gastos com a Copa.

## O que é usado?

* Módulo `urllib`  para download do arquivo zip dos dados.
* Módulo `io` - `FileIO`, `StringIO`
* Módulo `os` - `listdir()`, `chdir()`, `mkdir()`, `rename()`
* Módulo `os.path` - `join()`, `exists()`
* Módulo `zipfile` - `ZipFile`, `extractall()`, `close()`
* Módulo `pickle` - `dumps()`, `loads()`
* Múdolo `sys` - `argv`

## Processamento de Meta Dados

Download de uma base mensal

```sh
python download_dados_copa.py
```

Extraindo todos arquivos

```sh
python extrai_banco.py
```

Le meta dados

```sh
python le_meta_dados.py
```

Gera modelo visual

```sh
python analise_meta.py > relacionamentos.dot
dot -T png relacionamentos.dot -o relacionamentos.png
```

Detalhes de uma tabela?

```sh
python detalhe_tabela.py [NomeTabela]
PK  IdEmpreendimento               Tipo bigint
Col DescEmpreendimento             Tipo varchar
FK  IdCidadeSede                   Tipo bigint
FK  IdTema                         Tipo bigint
FK  IdAgrupador                    Tipo bigint
Col FlgFonteMatriz                 Tipo bit
Col FlgDireto                      Tipo bit
Col DescObservacao                 Tipo varchar
FK  IdAndamento                    Tipo bigint
Col FlgAtivo                       Tipo bit
FK  IdFaseGrupo                    Tipo bigint
Col TxtExplicativoInvestimento     Tipo varchar
Col TxtExplicativoRecursos         Tipo varchar
Col TxtExplicativoEtapas           Tipo varchar
FK  IdProjeto                      Tipo bigint
FK  IdInstituicao                  Tipo bigint
Col ValTotalPrevisto               Tipo numeric
Empreendimento -> Outras
[   ('CidadeSede', 'IdCidadeSede'),
    ('Tema', 'IdTema'),
    ('Agrupador', 'IdAgrupador'),
    ('Andamento', 'IdAndamento'),
    ('FaseGrupo', 'IdFaseGrupo'),
    ('Projeto', 'IdProjeto'),
    ('Instituicao', 'IdInstituicao')]
Outras -> Empreendimento
[   ('Alerta', 'IdAlerta'),
    ('Log', 'IdLog'),
    ('RelatorioExecucao', 'IdRelatorioExecucao'),
    ('Licenca', 'IdLicenca'),
    ('RecursoPrevisto', 'IdRecursoPrevisto'),
    ('ExecucaoFinanceira', 'IdExecucaoFinanceira'),
    ('Licitacao', 'IdLicitacao'),
    ('Etapa', 'IdEtapa'),
    ('Recurso', 'IdRecurso'),
    ('RecursoCaptado', 'IdRecursoCaptado')]
```

Dados de uma tabela?

```sh
python le_dados.py [NomeTabela]
```
