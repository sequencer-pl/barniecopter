import logging
import sqlite3


class SQLite3:
    def __init__(self):
        self.db = sqlite3.connect('database/barniecopter.db')

    def save(self, table, data):
        try:
            self._insert_data(table, data)
        except BaseException as err:
            if 'no such table' in str(err):
                self._create_table(table, data)
                self._insert_data(table, data)
            else:
                logging.error("Problem with insert data to db: %s", err)

    def _insert_data(self, table, data):
        self.db.execute("INSERT INTO %s(%s) VALUES (%s);" %
                        (table, ", ".join(data.keys()), "'{}'".format("', '".join(data.values()))))
        logging.debug(f"Data {data} inserted to {table}")

    def _create_table(self, table, data):
        self.db.execute("CREATE TABLE %s(%s)" % (table, ", ".join(data.keys())))
        logging.debug(f"New table {table} created")
