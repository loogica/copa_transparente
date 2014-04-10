class Query:
    def __init__(self, cols):
        self._cols = cols

    def _from(self, *args):
        n_tables = len(args)
        if n_tables > 1:
            raise Exception("Não implementado")

        cols = self._cols

        if n_tables == 1:
            return args[0]._select(cols)

def select(*args):
    return Query(args)

