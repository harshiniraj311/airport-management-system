import tkinter as tk
from tkinter import messagebox
from typing import List
import schedule
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import sqlite3

class Flight:
    def __init__(self, flight_id: int, flight_number: str, arrival_time: int, burst_time: int):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.completion_time = 0
        self.boarded_passengers = []

class Passenger:
    def __init__(self, flight_number: str, passenger_name: str):
        self.flight_number = flight_number
        self.passenger_name = passenger_name

class AirportManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Airport Management System")
        self.root.geometry("800x600")

        self.create_widgets()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.running = True
        threading.Thread(target=self.run_scheduler).start()

    def create_widgets(self):
        # Main title
        title_label = tk.Label(self.root, text="Airport Management System", font=("Helvetica", 18))
        title_label.pack(pady=10)

        # Flight management frame
        flight_frame = tk.LabelFrame(self.root, text="Flight Management", font=("Helvetica", 12))
        flight_frame.pack(pady=10, padx=20, fill="both", expand="yes")

        # Flight number entry
        flight_number_label = tk.Label(flight_frame, text="Flight Number:", font=("Helvetica", 10))
        flight_number_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.flight_number_entry = tk.Entry(flight_frame, font=("Helvetica", 10))
        self.flight_number_entry.grid(row=0, column=1, padx=10, pady=5)

        # Arrival time entry
        arrival_time_label = tk.Label(flight_frame, text="Arrival Time:", font=("Helvetica", 10))
        arrival_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.arrival_time_entry = tk.Entry(flight_frame, font=("Helvetica", 10))
        self.arrival_time_entry.grid(row=1, column=1, padx=10, pady=5)

        # Burst time entry
        burst_time_label = tk.Label(flight_frame, text="Burst Time (mins):", font=("Helvetica", 10))
        burst_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.burst_time_entry = tk.Entry(flight_frame, font=("Helvetica", 10))
        self.burst_time_entry.grid(row=2, column=1, padx=10, pady=5)

        # Flight management buttons
        add_flight_button = tk.Button(flight_frame, text="Add Flight", command=self.add_flight, font=("Helvetica", 10))
        add_flight_button.grid(row=3, column=0, columnspan=2, pady=5)

        delete_flight_button = tk.Button(flight_frame, text="Delete Flight", command=self.delete_flight, font=("Helvetica", 10))
        delete_flight_button.grid(row=4, column=0, columnspan=2, pady=5)

        view_flights_button = tk.Button(flight_frame, text="View Flights", command=self.view_flights, font=("Helvetica", 10))
        view_flights_button.grid(row=5, column=0, columnspan=2, pady=5)

        schedule_flights_button = tk.Button(flight_frame, text="Schedule Flights", command=self.schedule_flights, font=("Helvetica", 10))
        schedule_flights_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Passenger management frame
        passenger_frame = tk.LabelFrame(self.root, text="Passenger Management", font=("Helvetica", 12))
        passenger_frame.pack(pady=10, padx=20, fill="both", expand="yes")

        # Passenger name entry
        passenger_name_label = tk.Label(passenger_frame, text="Passenger Name:", font=("Helvetica", 10))
        passenger_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.passenger_name_entry = tk.Entry(passenger_frame, font=("Helvetica", 10))
        self.passenger_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Passenger flight number entry
        passenger_flight_number_label = tk.Label(passenger_frame, text="Flight Number:", font=("Helvetica", 10))
        passenger_flight_number_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.passenger_flight_number_entry = tk.Entry(passenger_frame, font=("Helvetica", 10))
        self.passenger_flight_number_entry.grid(row=1, column=1, padx=10, pady=5)

        # Passenger management buttons
        add_passenger_button = tk.Button(passenger_frame, text="Add Passenger", command=self.add_passenger, font=("Helvetica", 10))
        add_passenger_button.grid(row=2, column=0, columnspan=2, pady=5)

        delete_passenger_button = tk.Button(passenger_frame, text="Delete Passenger", command=self.delete_passenger, font=("Helvetica", 10))
        delete_passenger_button.grid(row=3, column=0, columnspan=2, pady=5)

        view_passengers_button = tk.Button(passenger_frame, text="View Passengers", command=self.view_passengers, font=("Helvetica", 10))
        view_passengers_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_program, font=("Helvetica", 12))
        exit_button.pack(pady=20)


    def add_flight(self):
        flight_number = self.flight_number_entry.get()
        arrival_time = self.arrival_time_entry.get()
        burst_time = self.burst_time_entry.get()

        if not flight_number or not arrival_time or not burst_time:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        add_flight(flight_number, int(arrival_time), int(burst_time))
        messagebox.showinfo("Info", "Flight added successfully")

    def delete_flight(self):
        flight_number = self.flight_number_entry.get()
        if not flight_number:
            messagebox.showwarning("Warning", "Please enter the flight number.")
            return
        delete_flight(flight_number)
        messagebox.showinfo("Info", "Flight deleted successfully")

    def add_passenger(self):
        passenger_name = self.passenger_name_entry.get()
        flight_number = self.passenger_flight_number_entry.get()

        if not passenger_name or not flight_number:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        add_passenger(flight_number, passenger_name)
        messagebox.showinfo("Info", "Passenger added successfully")

    def delete_passenger(self):
        passenger_name = self.passenger_name_entry.get()
        flight_number = self.passenger_flight_number_entry.get()
        
        if not passenger_name or not flight_number:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        delete_passenger(flight_number, passenger_name)
        messagebox.showinfo("Info", "Passenger deleted successfully")

    def view_flights(self):
        flights = get_flights()
        if not flights:
            messagebox.showinfo("Flights", "No flights available.")
            return
        flight_info = "\n".join([f"Flight Number: {flight[1]}, Arrival Time: {flight[2]}, Burst Time: {flight[3]}" for flight in flights])
        messagebox.showinfo("Flights", flight_info)

    def view_passengers(self):
        passengers = get_passengers()
        if not passengers:
            messagebox.showinfo("Passengers", "No passengers available.")
            return
        passenger_info = "\n".join([f"Passenger Name: {passenger[2]}, Flight Number: {passenger[1]}" for passenger in passengers])
        messagebox.showinfo("Passengers", passenger_info)

    def schedule_flights(self):
        flights = get_flights()
        if not flights:
            messagebox.showinfo("Scheduled Flights", "No flights available to schedule.")
            return

        flight_objects = [Flight(flight[0], flight[1], flight[2], flight[3]) for flight in flights]
        self.fcfs(flight_objects)

        flight_objects.sort(key=lambda x: x.completion_time)
        flight_info = "\n".join([
            f"Flight {flight.flight_number} - Arrival: {flight.arrival_time}, Departure: {flight.completion_time} {'(Delayed by ' + str((flight.completion_time - flight.arrival_time) - flight.burst_time) + ' mins)' if (flight.completion_time - flight.arrival_time) > flight.burst_time else '(On time)'}" 
            for flight in flight_objects
        ])
        
        messagebox.showinfo("Scheduled Flights", flight_info)

    def fcfs(self, flights: List[Flight]):
        flights.sort(key=lambda x: x.arrival_time)
        seen_completion_times = {}

        for flight in flights:
            flight.waiting_time = 0

            # Calculate initial completion time
            flight.completion_time = flight.arrival_time + flight.burst_time

            # Ensure unique completion time by adding 15 minutes in case of a collision
            while flight.completion_time in seen_completion_times:
                flight.completion_time += 15

            # Mark this completion time as seen
            seen_completion_times[flight.completion_time] = True

            # Update the flight record with the new waiting time and completion time
            update_flight(flight.flight_id, flight.waiting_time, flight.completion_time)

    def run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def exit_program(self):
        self.running = False
        self.executor.shutdown(wait=False)
        self.root.destroy()

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
                        passenger_name TEXT
                      )''')
    conn.commit()
    conn.close()

def add_flight(flight_number: str, arrival_time: int, burst_time: int):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flights (flight_number, arrival_time, burst_time) VALUES (?, ?, ?)", (flight_number, arrival_time, burst_time))
    conn.commit()
    conn.close()

def delete_flight(flight_number: str):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flights WHERE flight_number=?", (flight_number,))
    cursor.execute("DELETE FROM passengers WHERE flight_number=?", (flight_number,))
    conn.commit()
    conn.close()

def add_passenger(flight_number: str, passenger_name: str):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passengers (flight_number, passenger_name) VALUES (?, ?)", (flight_number, passenger_name))
    conn.commit()
    conn.close()

def delete_passenger(flight_number: str, passenger_name: str):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passengers WHERE flight_number=? AND passenger_name=?", (flight_number, passenger_name))
    conn.commit()
    conn.close()

def get_flights():
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    conn.close()
    return flights

def get_passengers():
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passengers")
    passengers = cursor.fetchall()
    conn.close()
    return passengers

def update_flight(flight_id: int, waiting_time: int, completion_time: int):
    conn = sqlite3.connect('airport.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE flights SET waiting_time=?, completion_time=? WHERE id=?", (waiting_time, completion_time, flight_id))
    conn.commit()
    conn.close()

def main():
    setup_database()
    root = tk.Tk()
    app = AirportManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
