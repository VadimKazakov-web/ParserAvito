# -*- coding: utf-8 -*-
import sqlite3
import logging
from settings import *
import re


class DataBaseMixin:

    def __init__(self):
        self._db = DATABASE
        self._table_name = "announcement"
        self.count_new_row_in_database = 0
        self.count_update_row_in_database = 0
        self._connection = None
        self._cursor = None
        self.total_result_db = None
        self.count_row_db = None
        self._pattern_already_exists_table = re.compile(r'already exists')
        self._database_init()
        self._count_row_in_database()

    def _connect_database(self):
        self._connection = sqlite3.connect(self._db)
        self._cursor = self._connection.cursor()

    def _database_init(self):
        try:
            self._create_database()
        except sqlite3.OperationalError as err:
            logging.warning(err)
            if self._pattern_already_exists_table.search(err.args[0]):
                # self.total_result_db = self.extraction_and_sorting()
                # self._count_row_in_database()
                self._delete_table()
                self._create_database()

    def _create_database(self):
        self._connect_database()
        # привязки (? или :name) не работают
        self._cursor.execute(
            "CREATE TABLE {} (id INTEGER, title TEXT, link TEXT, total_views, today_views, rating, reviews);".format(self._table_name))
        self._connection.commit()
        self._connection.close()

    def _delete_table(self):
        self._connect_database()
        self._cursor.execute(
            "DROP TABLE {}".format(self._table_name))
        self._connection.commit()
        self._connection.close()

    def _count_row_in_database(self):
        self._connect_database()
        res = self._cursor.execute("SELECT count(*) FROM announcement")
        result = res.fetchone()
        self.count_row_db = int(result[0])
        logging.info("count row in database: {}".format(self.count_row_db))

    def insert_in_database(self, data):
        self._connect_database()
        self._cursor.execute(
            "INSERT INTO announcement VALUES(:id, :title, :link, :total_views, :today_views, :rating, :reviews);",
            data)
        self.count_new_row_in_database += 1
        self._connection.commit()
        self._connection.close()

    def _list_tuple_in_list_dict(self, data):
        result_list = []
        for _id, title, link, total_views, today_views, rating, reviews in data:
            result_list.append({
                "id": _id,
                "title": title,
                "link": link,
                "total_views": total_views,
                "today_views": today_views,
                "rating": rating,
                "reviews": reviews,
            })
        return result_list

    def extraction_and_sorting(self):
        self._connect_database()

        total_views_res = self._cursor.execute("SELECT * FROM {} ORDER BY total_views DESC LIMIT {};".format(
            self._table_name, TOP_ANNOUNCEMENT))
        total_views_sort = self._list_tuple_in_list_dict(total_views_res.fetchall())

        today_views_res = self._cursor.execute("SELECT * FROM {} ORDER BY today_views DESC LIMIT {};".format(
            self._table_name, TOP_ANNOUNCEMENT))
        today_views_sort = self._list_tuple_in_list_dict(today_views_res.fetchall())

        reviews_res = self._cursor.execute("SELECT * FROM {} ORDER BY reviews DESC LIMIT {};".format(
            self._table_name, TOP_ANNOUNCEMENT))
        reviews_sort = self._list_tuple_in_list_dict(reviews_res.fetchall())

        result = {
            "total_views": total_views_sort,
            "today_views": today_views_sort,
            "reviews": reviews_sort,
        }
        self._connection.close()
        return result

    def record_in_database(self, data):
        self._connect_database()
        res = self._cursor.execute("SELECT * FROM announcement WHERE id = :id;", data)
        result = res.fetchone()
        if not result:
            self._cursor.execute(
                "INSERT INTO announcement VALUES(:id, :title, :link, :total_views, :today_views, :rating, :reviews);",
                data)
            self.count_new_row_in_database += 1

        else:
            self._cursor.execute(
                "UPDATE announcement SET title=:title, link=:link, total_views=:total_views, today_views=:today_views, rating=:rating, "
                "reviews=:reviews WHERE id=:id",
                data)
            self.count_update_row_in_database += 1
        self._connection.commit()
        self._connection.close()
