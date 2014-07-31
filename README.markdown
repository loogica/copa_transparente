# Copa Transparente

O projeto `copa transparente` é uma aplicação Livre, feita para Python 3.3 (ou superior)
que:

* Faz o download de um arquivo de banco de dados atualizado.
* Lê os arquivos de meta-dados e entende campos e relacionamentos do modelo
  pelos arquivos de meta dados.
* Gera um modelo visual das tabelas e relacionamentos (gera um .dot e depois um png)
* Lista a descrição da tabela - colunas com tipo de chave (primaria, estrangeira ou normal)
  e tipo do dado (string, int, etc...)
* Le linhas de um arquivo de banco.

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

## Obtendo a url para download

Para acessar os dados de todas as tabelas do dia dd/MM/yyyy,
onde dd representa o dia do mês (incluindo o 0 a esquerda,
se for dia de 1 a 9), MM representa o mês (incluindoo 0 a
esquerda, se for mês de 1 a 9) e yyyy o ano, basta acessar
o seguinte link:

http://www.portaldatransparencia.gov.br/copa2014/gestor/download?nomeArquivo=yyyyMMdd_BaseDados.zip

Exemplo: http://www.portaldatransparencia.gov.br/copa2014/gestor/download?nomeArquivo=20140110_BaseDados.zip

## Download de uma base de dados

```sh
python download.py url
```

Exemplo:

```sh
python download.py http://www.portaldatransparencia.gov.br/copa2014/gestor/download\?nomeArquivo\=20140729_BaseDados.zip
```

## Gera modelo visual

```sh
python analise_meta.py > relacionamentos.dot
dot -T png relacionamentos.dot -o relacionamentos.png
```

## Listando nomes das tabelas

```sh
python lista_tabelas.py
```


## Detalhes de uma tabela?

```sh
python detalhe_tabela.py [NomeTabela]
PK  IdExecucaoFinanceira           Tipo bigint
Col NumDocumento                   Tipo varchar
FK  IdAndamentoFinanceiro          Tipo bigint
FK  IdTipoExecucaoFinanceira       Tipo bigint
Col DatAssinatura                  Tipo datetime
Col DatInicioVigencia              Tipo datetime
Col DatFinalVigencia               Tipo datetime
Col IdInstituicaoContratante       Tipo bigint
FK  IdTipoDocumento                Tipo bigint
Col IdInstituicaoContratado        Tipo bigint
Col IdPessoaFisicaContratado       Tipo bigint
Col ValContrato                    Tipo decimal
Col ValContrapartida               Tipo decimal
Col ValTotal                       Tipo decimal
Col DescObjeto                     Tipo varchar
FK  IdLicitacao                    Tipo bigint
Col FlgInexibilidadeLicitacao      Tipo bit
Col FlgDispensaLicitacao           Tipo bit
FK  IdFundamentoLegal              Tipo bigint
FK  IdFaseGrupo                    Tipo bigint
Col FlgAtivo                       Tipo bit
Col FlgExclusaoDependencia         Tipo bit
ExecucaoFinanceira -> Outras
   ExecucaoFinanceira to ExecucaoFinanceira
   ExecucaoFinanceira to Empreendimento
   ExecucaoFinanceira to AndamentoFinanceiro
   ExecucaoFinanceira to TipoExecucaoFinanceira
   ExecucaoFinanceira to TipoDocumento
   ExecucaoFinanceira to Licitacao
   ExecucaoFinanceira to FundamentoLegal
   ExecucaoFinanceira to FaseGrupo
Outras -> ExecucaoFinanceira
   Desembolso to ExecucaoFinanceira
   Log to ExecucaoFinanceira
   Alerta to ExecucaoFinanceira
   Aditivo to ExecucaoFinanceira
```

## Dados de uma tabela?

```sh
python le_dados.py [NomeTabela]
```
