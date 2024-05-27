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
        self.burst_time = 0
