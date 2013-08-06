# Copa Transparente

O projeto `copa transparente` é uma aplicação Livre, feita para Python 3.3 (ou superior)
que:

* Faz o download de um arquivo de banco de dados atualizado.
* Lê os arquivos de meta-dados e criar entender os campos e relacionamentos do modelo
  pelos arquivos de meta dados.
* Gera um modelo visual das tabelas e relacionamentos (gerar um .dot e depois um png)
* Lista a descrição da tabela - colunas com tipo de chave (primaria, estrangeira ou normal)
  e tipo do dado (string, int, etc...)
* Ler linhas de um arquivo de banco.

## Próximos passos

* Criar visualizações gráficas desses dados, também compatível com Python 3.
* Deploy na web

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
