############################# IMPORTS #############################

import datetime
from flask import Flask, request

############################# GLOBAL VARIABLES #############################

tickets = []
previous_ticket_id = 1997
app = Flask(__name__)

############################# CLASSES #############################

class ParkingTicket:
    def __init__(self, plate, parking_lot, ticket_id):
        self.plate = plate
        self.parking_lot = parking_lot
        self.ticket_id = ticket_id
        self.parking_time = datetime.datetime.now()

    def __str__(self):
        plate = self.plate
        parking_lot = self.parking_lot
        total_parked_time = self.get_parking_time()
        charge = self.compute_charge()
        return f'''Plate: {plate}
Parking lot: {parking_lot}
Total parked time: {total_parked_time}
Charge: {charge}'''

    def get_parking_time(self):
        elapsed_time = datetime.datetime.now() - self.parking_time
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02}:{minutes:02}:{seconds:02}'

    def compute_charge(self):
        elapsed_time = datetime.datetime.now() - self.parking_time
        total_minutes = int(elapsed_time.total_seconds() / 60)
        quarters = total_minutes // 15
        charge = quarters * 2.5
        return f'${charge:.2f}'

############################# ENDPOINTS #############################

# For checking if the server is working properly
@app.route('/')
def hello():
     return 'Hello, World!'

# Endpoint to create a new parking ticket
@app.route('/entry', methods=['POST'])
def create_ticket():
    global previous_ticket_id
    global tickets
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')
    ticket_id = str(previous_ticket_id + 1)
    previous_ticket_id += 1
    new_ticket = ParkingTicket(plate, parking_lot, ticket_id)
    tickets.append(new_ticket)
    return str(ticket_id)

# Endpoint to close a parking ticket and calculate charges
@app.route('/exit', methods=['POST'])
def close_ticket():
    ticket_id = request.args.get('ticketId')

    ticket_instance = None
    for ticket in tickets:
        if ticket.ticket_id == ticket_id:
            ticket_instance = ticket
            break

    if ticket_instance is None:
        return 'Ticket not found'

    tickets.remove(ticket_instance)
    return str(ticket_instance)

#############################  #############################

if __name__ == '__main__': app.run()
