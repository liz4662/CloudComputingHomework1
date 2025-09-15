from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.passenger import PassengerCreate, PassengerRead, PassengerUpdate
from models.flight import FlightCreate, FlightRead, FlightUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
passengers: Dict[UUID, PassengerRead] = {}
flights: Dict[UUID, FlightRead] = {}

app = FastAPI(
    title="Passenger/Flight API",
    description="Demo FastAPI app using Pydantic v2 models for Passenger and Flight",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Flight endpoints
# -----------------------------------------------------------------------------

@app.post("/flights", response_model=FlightRead, status_code=201)
def create_flight(flight: FlightCreate):
    if flight.id in flights:
        raise HTTPException(status_code=400, detail="Flight with this ID already exists")
    flights[flight.id] = FlightRead(**flight.model_dump())
    return flights[flight.id]


@app.get("/flights", response_model=List[FlightRead])
def list_flights(
    flightNumber: Optional[str] = Query(None, description="Filter by flight number"),
    boardingTime: Optional[str] = Query(None, description="Filter by boarding time"),
    departureTime: Optional[str] = Query(None, description="Filter by departure time"),
    arrivalTime: Optional[str] = Query(None, description="Filter by arrival time"),
    departureAirport: Optional[str] = Query(None, description="Filter by departure airport"),
    arrivalAirport: Optional[str] = Query(None, description="Filter by arrival airport"),
):
    results = list(flights.values())

    if flightNumber is not None:
        results = [a for a in results if a.flightNumber == flightNumber]
    if boardingTime is not None:
        results = [a for a in results if a.boardingTime == boardingTime]
    if departureTime is not None:
        results = [a for a in results if a.departureTime == departureTime]
    if arrivalTime is not None:
        results = [a for a in results if a.arrivalTime == arrivalTime]
    if departureAirport is not None:
        results = [a for a in results if a.departureAirport == departureAirport]
    if arrivalAirport is not None:
        results = [a for a in results if a.arrivalAirport == arrivalAirport]


    return results

@app.get("/flights/{flight_id}", response_model=FlightRead)
def get_flight(flight_id: UUID):
    if flight_id not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flights[flight_id]

@app.patch("/flights/{flight_id}", response_model=FlightRead)
def update_flight(flight_id: UUID, update: FlightUpdate):
    if flight_id not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")
    stored = flights[flight_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    flights[flight_id] = FlightRead(**stored)
    return flights[flight_id]

@app.delete("/flights/{flight_id}", status_code=204)
def delete_flight(flight_id: UUID):
    if flight_id not in flights:
        raise HTTPException(status_code=404, detail="Flight not found")
    del flights[flight_id]
    return None

# -----------------------------------------------------------------------------
# Passenger endpoints
# -----------------------------------------------------------------------------
@app.post("/passengers", response_model=PassengerRead, status_code=201)
def create_passenger(passenger: PassengerCreate):
    # Each passenger gets its own UUID; stored as PassengerRead
    passenger_read = PassengerRead(**passenger.model_dump())
    passengers[passenger_read.id] = passenger_read
    return passenger_read

@app.get("/passengers", response_model=List[PassengerRead])
def list_passengers(
    firstName: Optional[str] = Query(None, description="Filter by first name"),
    lastName: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birthDate: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
):
    results = list(passengers.values())

    if firstName is not None:
        results = [p for p in results if p.firstName == firstName]
    if lastName is not None:
        results = [p for p in results if p.lastName == lastName]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birthDate is not None:
        results = [p for p in results if str(p.birthDate) == birthDate]

    return results

@app.get("/passengers/{passenger_id}", response_model=PassengerRead)
def get_passenger(passenger_id: UUID):
    if passenger_id not in passengers:
        raise HTTPException(status_code=404, detail="{passenger_id} not found")
    return passengers[passenger_id]

@app.patch("/passengers/{passenger_id}", response_model=PassengerRead)
def update_passenger(passenger_id: UUID, update: PassengerUpdate):
    if passenger_id not in passengers:
        raise HTTPException(status_code=404, detail="Passenger not found")
    stored = passengers[passenger_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    passengers[passenger_id] = PassengerRead(**stored)
    return passengers[passenger_id]

@app.delete("/passengers/{passenger_id}", status_code=204)
def delete_passenger(passenger_id: UUID):
    if passenger_id not in passengers:
        raise HTTPException(status_code=404, detail="Passenger not found")
    del passengers[passenger_id]
    return None


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Passenger/Flight API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
