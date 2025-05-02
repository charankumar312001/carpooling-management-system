import subprocess
from utils import DBAccess

def create_tables():
    queries = [
        """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(255),
            email VARCHAR(100) UNIQUE,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20),
            is_driver BOOLEAN DEFAULT FALSE
        )""",
        """CREATE TABLE IF NOT EXISTS rides (
            id INT AUTO_INCREMENT PRIMARY KEY,
            driver_id INT,
            start_location VARCHAR(100),
            destination VARCHAR(100),
            departure_time DATETIME,
            arrival_time DATETIME,
            available_seats INT,
            price DECIMAL(6,2),
            FOREIGN KEY (driver_id) REFERENCES users(id)
        )""",
        """CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ride_id INT,
            passenger_id INT,
            status ENUM('pending', 'confirmed', 'cancelled'),
            FOREIGN KEY (ride_id) REFERENCES rides(id),
            FOREIGN KEY (passenger_id) REFERENCES users(id)
        )"""
    ]
    
    try:
        for query in queries:
            DBAccess.execute_update(query)
    except Exception as e:
        print("Database error:", e)

if __name__ == "__main__":
    create_tables()
    subprocess.Popen(['python.exe', 'home.py'])
