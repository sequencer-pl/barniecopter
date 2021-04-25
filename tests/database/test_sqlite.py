from unittest import TestCase, mock
from unittest.mock import call

import callee as callee

from database.sqlite import SQLite3


class SQLite3Test(TestCase):

    @mock.patch('database.sqlite.sqlite3')
    def test_save_create_table_if_not_exists_and_then_insert_to_created_table_passed_data_to_queries(self, sqlite3):
        # given
        db = mock.MagicMock()
        sqlite3.connect.return_value = db
        db.execute.side_effect = (BaseException("no such table"), None, None)
        data = {'some': 'thing', 'any': 'one'}
        table_name = 'BTC'

        # when
        SQLite3().save(table=table_name, data=data)

        # then
        db.execute.assert_has_calls([
            call(callee.String() & callee.StartsWith("INSERT INTO")
                 & callee.Contains(table_name) & callee.Contains(", ".join(data.keys()))
                 & callee.Contains(data.get('some')) & callee.Contains(data.get('any'))),

            call(callee.String() & callee.StartsWith("CREATE TABLE")
                 & callee.Contains(table_name) & callee.Contains(", ".join(data.keys()))),

            call(callee.String() & callee.StartsWith("INSERT INTO")
                 & callee.Contains(table_name) & callee.Contains(", ".join(data.keys()))
                 & callee.Contains(data.get('some')) & callee.Contains(data.get('any'))),
        ])
