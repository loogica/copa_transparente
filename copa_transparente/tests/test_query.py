import decimal
import unittest

from copa_transparente.query import select
from copa_transparente import domain

class QueryTest(unittest.TestCase):
    def test_select(self):
        a_table = domain.DataTable('ExecucaoFinanceira')
        col = a_table.add_column('Id', 'bigint')
        col2 = a_table.add_column('Value', 'decimal')

        a_table._data = [(1, decimal.Decimal("0.0")),
                         (2, decimal.Decimal("1.0"))]

        result = list(select("Id")._from(a_table))
        self.assertEqual([(1, ), (2, )], result)

    def test_select_2_names(self):
        a_table = domain.DataTable('ExecucaoFinanceira')
        col = a_table.add_column('Id', 'bigint')
        col2 = a_table.add_column('Value', 'decimal')

        a_table._data = [(1, decimal.Decimal("0.0")),
                         (2, decimal.Decimal("1.0"))]

        result = list(select("Id", "Value")._from(a_table))
        self.assertEqual([(1, decimal.Decimal("0.0")),
                          (2, decimal.Decimal("1.0"))], result)
