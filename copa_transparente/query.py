from copa_transparente.commands import extracao

class Query:
    def __init__(self, cols):
        self._cols = cols

    def from_table(self, *args):
        return self.from_tables(*args)

    def from_tables(self, *args, on=None):
        n_tables = len(args)
        if n_tables == 0:
            raise Exception("Especificar pelo menos uma tabela")

        cols = self._cols

        tables = []
        for i in range(n_tables):
            tables.append(extracao.load_table(args[i]))

        if n_tables == 1:
            return tables[0]._select(cols)
        else:
            return (tables[0]._join(tables[1], on=on))._select(cols)

def select(*args):
    return Query(args)

