from src.api_adapter import APIAdapter
from src.database import DBManager


class DataLoader:
    """Сервис загрузки стран и самолетов в БД."""

    def __init__(self):
        self.api = APIAdapter()
        self.db = DBManager()

    def save_country(self, country: str):
        """Сохраняет страну в БД."""

        country_data = self.api.get_country(country)

        if not country_data:
            print(f"Страна {country} не найдена")
            return

        db_connection = self.db.connect()
        db_cursor = db_connection.cursor()

        db_cursor.execute("""
            INSERT INTO countries (
                name,
                bbox_min_lat,
                bbox_max_lat,
                bbox_min_lon,
                bbox_max_lon
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
        """, (
            country,
            float(country_data[0]),
            float(country_data[1]),
            float(country_data[2]),
            float(country_data[3]),
        ))

        db_connection.commit()
        db_cursor.close()
        db_connection.close()

        print(f"Страна {country} сохранена")

    def save_aircraft(self, country: str):
        """Сохраняет самолеты в БД."""

        data = self.api.get_aeroplanes(country)
        planes = data.get("states", [])

        if not planes:
            print(f"Самолеты для {country} не найдены")
            return

        db_connection = self.db.connect()
        db_cursor = db_connection.cursor()

        for plane in planes:
            db_cursor.execute("""
                INSERT INTO aircraft (
                    icao24,
                    callsign,
                    origin_country,
                    longitude,
                    latitude,
                    altitude,
                    velocity,
                    heading,
                    on_ground,
                    timestamp
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, (
                plane[0],
                plane[1],
                plane[2],
                plane[5],
                plane[6],
                plane[7],
                plane[9],
                plane[10],
                plane[8],
                data["time"]
            ))

        db_connection.commit()
        db_cursor.close()
        db_connection.close()

        print(f"Самолеты для {country} сохранены")
