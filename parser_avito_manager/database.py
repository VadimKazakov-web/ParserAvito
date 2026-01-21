# -*- coding: utf-8 -*-
import sqlite3
import logging
from settings import *


class DataBaseMixin:

    def __init__(self):
        self._db = DATABASE
        self.count_new_row_in_database = 0
        self.count_update_row_in_database = 0
        self._connection = None
        self._cursor = None
        self._create_database()

    def _connect_database(self):
        self._connection = sqlite3.connect(self._db)
        self._cursor = self._connection.cursor()

    def _create_database(self):
        self._connect_database()
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS announcement(id INTEGER, title TEXT, link TEXT, total_views, rating, reviews)")
        self._connection.commit()
        self._connection.close()

    def count_row_in_database(self):
        self._connect_database()
        res = self._cursor.execute("SELECT count(*) FROM announcement")
        result = res.fetchone()
        count = int(result[0])
        logging.info("count row in database: {}".format(count))

    def record_in_database(self, data):
        self._connect_database()
        res = self._cursor.execute("SELECT * FROM announcement WHERE id = :id;", data)
        result = res.fetchone()
        if not result:
            self._cursor.execute(
                "INSERT INTO announcement VALUES(:id, :title, :link, :total_views, :rating, :reviews);",
                data)
            self.count_new_row_in_database += 1

        else:
            self._cursor.execute(
                "UPDATE announcement SET title=:title, link=:link, total_views=:total_views, rating=:rating, "
                "reviews=:reviews WHERE id=:id",
                data)
            self.count_update_row_in_database += 1
        self._connection.commit()
        self._connection.close()
