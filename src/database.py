import os

import psycopg2
from dotenv import load_dotenv


class DBManager:
    """Класс для работы с PostgreSQL."""

    def __init__(self):
        """
        Инициализация подключения к PostgreSQL.

        Загружает переменные окружения из .env файла и формирует
        параметры подключения к базе данных (dbname, user, password, host, port).
        """
        load_dotenv()

        self.conn_params = {
            "dbname": os.getenv("DBNAME"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "host": os.getenv("HOST"),
            "port": os.getenv("PORT"),
        }

    def connect(self):
        """Создает соединение с БД."""
        return psycopg2.connect(**self.conn_params)

    def create_tables(self):
        """Создание таблиц countries и aircraft."""

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    bbox_min_lat DOUBLE PRECISION,
                    bbox_max_lat DOUBLE PRECISION,
                    bbox_min_lon DOUBLE PRECISION,
                    bbox_max_lon DOUBLE PRECISION
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS aircraft (
                    id SERIAL PRIMARY KEY,
                    icao24 VARCHAR(10),
                    callsign VARCHAR(20),
                    origin_country VARCHAR(100),
                    longitude DOUBLE PRECISION,
                    latitude DOUBLE PRECISION,
                    altitude DOUBLE PRECISION,
                    velocity DOUBLE PRECISION,
                    heading DOUBLE PRECISION,
                    on_ground BOOLEAN,
                    timestamp BIGINT,
                    CONSTRAINT unique_aircraft_time UNIQUE (icao24, timestamp)
                );
            """)

            conn.commit()
            print("Таблицы успешно созданы")

        finally:
            cur.close()
            conn.close()

    def drop_tables(self):
        """Удаление таблиц."""
        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute("DROP TABLE IF EXISTS aircraft;")
            cur.execute("DROP TABLE IF EXISTS countries;")

            conn.commit()
            print("Таблицы удалены")

        finally:
            cur.close()
            conn.close()

    def get_countries_and_aeroplanes_count(self):
        """
        Получает список стран и количество самолетов в их воздушном пространстве.
        """

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT
                    origin_country,
                    COUNT(*)
                FROM aircraft
                GROUP BY origin_country;
            """)

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    def get_all_aeroplanes(self):
        """
        Получает список всех самолетов.
        """

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT *
                FROM aircraft;
            """)

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    def get_avg_speed(self):
        """
        Получает среднюю скорость самолетов.
        """

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT AVG(velocity)
                FROM aircraft
                WHERE velocity IS NOT NULL;
            """)

            return cur.fetchone()[0]

        finally:
            cur.close()
            conn.close()

    def get_aeroplanes_with_higher_speed(self):
        """
        Получает самолеты со скоростью выше средней.
        """

        avg_speed = self.get_avg_speed()

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                SELECT *
                FROM aircraft
                WHERE velocity > %s;
            """,
                (avg_speed,),
            )

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    def get_aeroplanes_with_keyword(self, keyword: str):
        """
        Получает список всех самолетов, в позывном которых содержатся переданные в метод символы
        Пример: 'ACA' — Air Canada.
        """

        conn = self.connect()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                SELECT *
                FROM aircraft
                WHERE callsign ILIKE %s;
            """,
                (f"%{keyword}%",),
            )

            return cur.fetchall()

        finally:
            cur.close()
            conn.close()
