import sqlite3

def setup_database():
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT,
                        arrival_time INTEGER,
                        burst_time INTEGER,
                        waiting_time INTEGER,
                        completion_time INTEGER
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS passengers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT,
                        passenger_name TEXT,
                        arrival_time INTEGER,
                        burst_time INTEGER
                      )''')
    conn.commit()
    conn.close()

def add_flight(flight_number, arrival_time, burst_time):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flights (flight_number, arrival_time, burst_time) VALUES (?, ?, ?)',
                   (flight_number, arrival_time, burst_time))
    conn.commit()
    conn.close()

def add_passenger(flight_number, passenger_name, arrival_time):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passengers (flight_number, passenger_name) VALUES (?, ?)',
                   (flight_number, passenger_name))
    conn.commit()
    conn.close()

def get_flights():
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights')
    flights = cursor.fetchall()
    conn.close()
    return flights

def get_passengers():
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passengers')
    passengers = cursor.fetchall()
    conn.close()
    return passengers

def update_flight(flight_id, waiting_time, completion_time):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE flights SET waiting_time = ?, completion_time = ? WHERE id = ?',
                   (waiting_time, completion_time, flight_id))
    conn.commit()
    conn.close()
