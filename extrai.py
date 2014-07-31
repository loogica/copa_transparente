from copa_transparente.commands import extracao

if __name__ == "__main__":
    import sys
    extracao.table_detail(sys.argv[1])
    extracao.table_list()
    extracao.show_data(sys.argv[1])

