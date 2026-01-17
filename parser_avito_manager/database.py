# -*- coding: utf-8 -*-
import sqlite3
import logging
from settings import *


class DataBaseMixin:
    _db = DATABASE
    _count_new_row_in_database = 0
    _count_update_row_in_database = 0

    @classmethod
    def connect_database(cls):
        cls.connection = sqlite3.connect(cls._db)
        cls.cursor = cls.connection.cursor()

    @classmethod
    def create_database(cls):
        cls.connect_database()
        cls.cursor.execute(
            "CREATE TABLE IF NOT EXISTS announcement(id INTEGER, title TEXT, link TEXT, total_views, rating, reviews)")
        cls.connection.commit()
        cls.connection.close()

    @classmethod
    def count_row_in_database(cls):
        cls.connect_database()
        res = cls.cursor.execute("SELECT count(*) FROM announcement")
        result = res.fetchone()
        count = int(result[0])
        logging.info("count row in database: {}".format(count))

    @classmethod
    def record_in_database(cls, data):
        cls.connect_database()
        res = cls.cursor.execute("SELECT * FROM announcement WHERE id = :id;", data)
        result = res.fetchone()
        if not result:
            cls.cursor.execute("INSERT INTO announcement VALUES(:id, :title, :link, :total_views, :rating, :reviews);",
                               data)
            cls._count_new_row_in_database += 1

        else:
            cls.cursor.execute(
                "UPDATE announcement SET title=:title, link=:link, total_views=:total_views, rating=:rating, "
                "reviews=:reviews WHERE id=:id",
                data)
            cls._count_update_row_in_database += 1
        cls.connection.commit()
        cls.connection.close()
