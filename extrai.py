# coding: utf-8

import argparse

from copa_transparente.commands import extracao


parser = argparse.ArgumentParser(description='Extrai informação dos dados',
                                 add_help=False)
parser.add_argument('-a', '--ajuda', action='help', help='Exibe ajuda')
parser.add_argument('-l', '--lista', required=False, action='store_const',
                    const=True, help='Lista tabelas')
parser.add_argument('-d', '--detalhe', type=str, required=False,
                    help='Descrição de uma tabela')
parser.add_argument('-c', '--consulta', type=str, required=False,
                    help='Consulta dados de uma tabela')
parser.add_argument('-g', '--dotlang', required=False, action='store_const',
                    const=True, help='Gerar saída dotlang para gerar imagem')


if __name__ == "__main__":
    args = parser.parse_args()
    if args.detalhe:
        extracao.table_detail(args.detalhe)
    elif args.lista:
        extracao.table_list()
    elif args.dotlang:
        extracao.generate_dotlang()
    else:
        extracao.show_data(args.consulta)
