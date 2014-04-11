# coding: utf-8
import decimal
import json
import sys
import unittest

class Column:
    """Representa uma coluna em um DataTable

       Essa classe contém as informações de uma coluna
       e deve validar um dado de acordo com o tipo de
       dado configurado no construtor.

       Attributes:
           name: Nome da Coluna
           kind: Tipo do Dado (varchar, bigint, numeric)
           description: Descrição da coluna
    """
    def __init__(self, name, kind, description=""):
        """Construtor

            Args:
                name: Nome da Coluna
                kind: Tipo do dado (varchar, bigint, numeric)
                description: Descrição da coluna
        """
        self._name = name
        self._kind = kind
        self._description = description
        self._is_pk = False

    def __str__(self):
        _str = "Col: {} : {} {}".format(self._name,
                                        self._kind,
                                        self._description)
        if self._is_pk:
            _str = "({}) {} : {}".format("PK", self._name, self._kind)
        return _str

    def __eq__(self, obj):
        return self._name == obj.name

    def __hash__(self):
        return hash((self._name,
                     self._description,
                     self._kind))

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def is_pk(self):
        return self._is_pk

    @staticmethod
    def validate(kind, data):
        if not data:
            return True
        if kind == 'bigint':
            if isinstance(data, str):
                try:
                    n = int(data)
                except ValueError:
                    return False
                return True
            elif isinstance(data, int):
                return True
            return False
        elif kind == 'varchar':
            if isinstance(data, str):
                return True
            return False
        elif kind == 'numeric' or kind == 'decimal':
            try:
                val = decimal.Decimal(data)
            except:
                return False
            return True
        elif kind == 'datetime':
            #TODO IMPLEMENTAR
            return True
        elif kind == 'bit':
            if data in ("FALSE", "TRUE"):
                return True
            return False

    @staticmethod
    def convert(kind, data):
        if kind == 'bigint':
            if not data:
                return None
            if isinstance(data, str):
                try:
                    n = int(data)
                except ValueError:
                    raise Exception("Conversão inválida")
                return n
            elif isinstance(data, int):
                return data
        elif kind == 'varchar':
            return str(data)
        elif kind == 'numeric' or kind == 'decimal':
            if not data:
                return decimal.Decimal("0")
            try:
                val = decimal.Decimal(data)
                return val
            except:
                pass
            raise Exception("Conversão inválida")
        elif kind == 'datetime':
            #TODO IMPLEMENTAR
            return data
        elif kind == 'bit':
            if not data:
                return None
            if data == "FALSE":
                return False
            elif data == "TRUE":
                return True
            raise Exception("Conversão inválida")


class PrimaryKey(Column):
    def __init__(self, name, kind, description=None):
        super().__init__(name, kind, description=description)
        self._is_pk = True


class Relationship:
    """Classe que representa um relacionamento entre DataTables

       Essa classe tem todas as informações que identificam um relacionamento
       entre tabelas. Em qual coluna ele existe, de onde vem e pra onde vai.
    """
    def __init__(self, name, _from, to, on):
        """Construtor

           Args:
               name: Nome
               from: Tabela de onde sai
               to: Tabela pra onde vai
               on: instância de coluna onde existe
        """
        self._name = name
        self._from = _from
        self._to = to
        self._on = on

    def __str__(self):
        return "{} to {}".format(self._from.name, self._to.name)

class DataTable:
    """Representa uma Tabela de dados.

       Essa classe representa uma tabela de dados do portal
       da transparência. Deve ser capaz de validar linhas
       inseridas de acordo com as colunas que possui.

       Attributes:
           name: Nome da tabela
           columns: [Lista de colunas]
    """
    def __init__(self, name):
        """Construtor

            Args:
                name: Nome da Tabela
        """
        self._name = name
        self._columns = []
        self._references = []
        self._referenced = []
        self._data = []

    def _get_name(self):
        return self._name

    def _set_name(self, _name):
        self._name = _name

    def _del_name(self):
        raise AttributeError("Não pode deletar esse atributo")

    name = property(_get_name, _set_name, _del_name)
    references = property(lambda self: self._references)
    referenced = property(lambda self: self._referenced)

    def add_column(self, name, kind, description=""):
        self._validate_kind(kind)
        column = Column(name, kind, description=description)
        self._columns.append(column)
        return column

    def add_pk(self, name, kind, description=""):
        self._validate_kind(kind)
        column = PrimaryKey(name, kind, description=description)
        self._columns.append(column)
        return column

    @property
    def pk(self):
        for col in self._columns:
            if col.is_pk:
                return col
        return None

    @property
    def cols(self):
        return self._columns

    def _validate_kind(self, kind):
        if not kind in ('bigint', 'numeric', 'varchar', 'datetime', 'decimal', 'bit',
                        'int', 'ntext'):
            raise Exception("Tipo {} inválido".format(kind))

    def add_references(self, name, to, on):
        """Cria uma referencia dessa tabela para uma outra tabela

           Args:
              name: nome da relação
              to: instância da tabela apontada
              on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, self, to, on)
        self._references.append(relationship)

    def add_referenced(self, name, by, on):
        """Cria uma referência para outra tabela que aponta para essa.

           Args:
              name: nome da relação
              by: instância da tabela que aponta para essa
              on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, by, self, on)
        self._referenced.append(relationship)

    def add_data(self, values):
        for i, (value, column) in enumerate(zip(values, self.cols)):
            validate = Column.validate(column.kind, value)
            if not validate:
                raise Exception("Data e Tipo Iválidos {} : {}".format(column.kind,
                                                                      value))
            converted_value = Column.convert(column.kind, value)
            values[i] = converted_value
        self._data.append(tuple(values))

    def _get_indexes(self, args):
        cols = []
        for name in args:
            for i, col in enumerate(self._columns):
                if name == col.name:
                    cols.append(i)
        if not cols:
            return list(range(len(self._columns)))

        return cols

    def _select(self, args):
        indexes = self._get_indexes(args)
        for data in self._data:
            row_data = []
            for i in indexes:
                row_data.append(data[i])
            yield tuple(row_data)
