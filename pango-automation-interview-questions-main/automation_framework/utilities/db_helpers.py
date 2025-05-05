import sqlite3

class DatabaseHelper:
    def __init__(self, db_name="data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't exist
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                temperature REAL,
                feels_like REAL,
                              average_temperature REAL
            )''')

    def insert_weather_data(self, city, temperature, feels_like, average_temperature):
        try:
            with self.conn:
                self.conn.execute('''INSERT OR REPLACE INTO weather_data
                                  (city, temperature, feels_like, average_tempurature)
                                  VALUES (?, ?, ?, ?)''',
                                  (city, temperature, feels_like, average_temperature))
            print(f"{city} updated")
        except sqlite3.Error as err:
            print(f"Database Error: {err}")
        

    def get_weather_data(self, city):
        try:
            cursor = self.conn.execute("SELECT temperature, feels_like, average_temperature FROM weather_data WHERE city=?", (city,))
            return cursor.fetchone()
        except sqlite3.Error as err:
            print(f"Database Error: {err}")

    def get_city_with_highest_avg_temp(self):
        try:
            cursor = self.conn.execute("SELECT city FROM weather_data ORDER BY average_temperature DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                return result[0] 
            else:
                return None 
        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return None
