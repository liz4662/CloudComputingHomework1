from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class FlightBase(BaseModel):
    flightNumber: str = Field(
        ...,
        description="Number of the flight.",
        json_schema_extra={"example": "UA1250"},
    )
    boardingTime: str = Field(
        ...,
        description="Time flight starts boarding passengers.",
        json_schema_extra={"example": "7:00AM"},
    )
    departureTime: str = Field(
        ...,
        description="Time flight departs.",
        json_schema_extra={"example": "7:32AM"},
    )
    arrivalTime: str = Field(
        None,
        description="Local time of flight's arrival.",
        json_schema_extra={"example": "11:38AM"},
    )
    departureAirport: str = Field(
        None,
        description="Airport flight departs from.",
        json_schema_extra={"example": "JFK"},
    )
    arrivalAirport: str = Field(
        ...,
        description="Airport the flight arrives to.",
        json_schema_extra={"example": "SFO"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "flightNumber": "UA1250",
                    "boardingTime": "7:00AM",
                    "departureTime": "7:32AM",
                    "arrivalTime": "11:38AM",
                    "departureAirport": "JFK",
                    "arrivalAirport": "SFO",
                }
            ]
        }
    }


class FlightCreate(FlightBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "flightNumber": "UA1234",
                    "boardingTime": "3:15PM",
                    "departureTime": "3:45PM",
                    "arrivalTime": "4:53PM",
                    "departureAirport": "LGA",
                    "arrivalAirport": "ORD",
                }
            ]
        }
    }


class FlightUpdate(BaseModel):
    """Partial update; flight ID is taken from the path, not the body."""
    flightNumber: Optional[str] = Field(
        None, description="Number of the flight.", json_schema_extra={"example": "UA7865"}
    )
    boardingTime: Optional[str] = Field(
        None, description="Time flight starts boarding passengers.", json_schema_extra={"example": "7:11PM"}
    )
    departureTime: Optional[str] = Field(
        None, description="Time flight departs.", json_schema_extra={"example": "7:59PM"}
    )
    arrivalTime: Optional[str] = Field(
        None, description="Local time of flight's arrival.", json_schema_extra={"example": "4:03AM"}
    )
    departureAirport: Optional[str] = Field(
        None, description="Airport flight departs from.", json_schema_extra={"example": "SJC"}
    )
    arrivalAirport: Optional[str] = Field(
        None, description="Airport the flight arrives to.", json_schema_extra={"example": "MIA"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "boardingTime": "8:00PM",
                    "departureTime": "8:30PM",
                    "arrivalTime": "4:45AM",
                },
                {"arrivalTime": "4:23AM"},
            ]
        }
    }


class FlightRead(FlightBase):
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Flight ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "flightNumber": "UA1234",
                    "boardingTime": "3:15PM",
                    "departureTime": "3:45PM",
                    "arrivalTime": "4:53PM",
                    "departureAirport": "LGA",
                    "arrivalAirport": "ORD",
                }
            ]
        }
    }
