# -*- coding: utf-8 -*-
import sqlite3
import logging
from settings import *


class Connection:
    _db = DATABASE
    _connection = None
    _cursor = None

    @classmethod
    def __enter__(cls):
        cls._connect_database()
        return cls._cursor

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls._connection.commit()
        cls._connection.close()

    @classmethod
    def _connect_database(cls):
        """
        Подключение к базе данных
        """
        cls._connection = sqlite3.connect(cls._db)
        cls._cursor = cls._connection.cursor()


def create_database():
    with Connection() as cursor:
        """
        Создание новой таблицы
        """
        # привязки (? или :name) не работают c CREATE TABLE
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (id INTEGER, title TEXT, link TEXT, total_views, today_views, rating, reviews);".format(DB_TABLE_NAME))


class DataBaseMixin:
    """
    Класс для работы с базой данных.
    При инициализации удаляется старая таблица и создаётся новая.
    Созданная таблица используется для хранения данных объявлений полученных из одной сессии.
    """
    _table_name = DB_TABLE_NAME
    create_database()

    def delete_table(self):
        with Connection() as cursor:
            """
            Удаление таблицы
            """
            cursor.execute(
                "DROP TABLE {}".format(self._table_name))

    @staticmethod
    def count_row_in_database():
        with Connection() as cursor:
            """
            Подсчёт объявлений в таблице
            """
            res = cursor.execute("SELECT count(*) FROM announcement")
            result = res.fetchone()
            return int(result[0])

    @classmethod
    def insert_in_database(cls, data: dict):
        with Connection() as cursor:
            """
            Вставка данных одного объявления в таблицу
            """
            result = cursor.execute("SELECT id FROM {} WHERE id = {}".format(cls._table_name, data.get("id")))
            if not result.fetchall():
                cursor.execute(
                    "INSERT OR IGNORE INTO announcement VALUES(:id, :title, :link, :total_views, :today_views, :rating, :reviews);",
                    data)

    @staticmethod
    def _list_tuple_in_list_dict(data):
        """
        Конвертация списка кортежей в список словарей
        """
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

    def extraction_and_sorting_generator(self):
        with Connection() as cursor:
            """
            Получение отсортированных объявлений
            """
            total_views_res = cursor.execute("SELECT * FROM {} ORDER BY total_views DESC LIMIT {};".format(
                self._table_name, TOP_ANNOUNCEMENT))
            total_views_sort = self._list_tuple_in_list_dict(total_views_res.fetchall())
            yield total_views_sort

            today_views_res = cursor.execute("SELECT * FROM {} ORDER BY today_views DESC LIMIT {};".format(
                self._table_name, TOP_ANNOUNCEMENT))
            today_views_sort = self._list_tuple_in_list_dict(today_views_res.fetchall())
            yield today_views_sort

            reviews_res = cursor.execute("SELECT * FROM {} ORDER BY reviews DESC LIMIT {};".format(
                self._table_name, TOP_ANNOUNCEMENT))
            reviews_sort = self._list_tuple_in_list_dict(reviews_res.fetchall())
            yield reviews_sort
