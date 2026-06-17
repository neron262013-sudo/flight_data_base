import os
import psycopg2
from dotenv import load_dotenv


class DBManager:
    """Класс для работы с PostgreSQL."""

    def __init__(self):
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
                timestamp BIGINT
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("Таблицы успешно созданы")

    def drop_tables(self):
        """Удаление таблиц (для пересоздания)."""
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS aircraft;")
        cur.execute("DROP TABLE IF EXISTS countries;")

        conn.commit()
        cur.close()
        conn.close()

        print("Таблицы удалены")


if __name__ == "__main__":
    db = DBManager()
    db.create_tables()