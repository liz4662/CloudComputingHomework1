from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr



class PassengerBase(BaseModel):
    firstName: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ada"},
    )
    lastName: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Lovelace"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "ada@example.com"},
    )
    phone: str = Field(
        ...,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example": "+1-212-555-0199"},
    )
    birthDate: date = Field(
        ...,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "1815-12-10"},
    )
    passportNumber: str = Field(
        ...,
        description="Passport number exactly as it appears.",
        json_schema_extra={"example": "A12345678"},
    )

    flights: List[UUID] = Field(
        default_factory=list,
        description="List of flight IDs this passenger is booked on.",
        json_schema_extra={"example": ["550e8400-e29b-41d4-a716-446655440000"]}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "firstName": "Ada",
                    "lastName": "Lovelace",
                    "email": "ada@example.com",
                    "phone": "+1-212-555-0199",
                    "birthDate": "1815-12-10",
                    "passportNumber": "A12345678",
                }
            ]
        }
    }


class PassengerCreate(PassengerBase):
    """Creation payload for a Passenger."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "firstName": "Grace",
                    "lastName": "Hopper",
                    "email": "grace.hopper@navy.mil",
                    "phone": "+1-202-555-0101",
                    "birthDate": "1906-12-09",
                    "passportNumber": "B12345678",
                    "flights": []
                }
            ]
        }
    }


class PassengerUpdate(BaseModel):
    """Partial update for a Passenger; supply only fields to change."""
    firstName: Optional[str] = Field(None, json_schema_extra={"example": "Augusta"})
    lastName: Optional[str] = Field(None, json_schema_extra={"example": "King"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ada@newmail.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+44 20 7946 0958"})
    birthDate: Optional[date] = Field(None, json_schema_extra={"example": "1815-12-10"})
    passportNumber: Optional[str] = Field(None, json_schema_extra={"example": "C12345678"})
    flights: Optional[List[UUID]] = Field(None, json_schema_extra={"example": ["550e8400-e29b-41d4-a716-446655440000"]})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"firstName": "Ada", "lastName": "Byron"},
                {"phone": "+1-415-555-0199"},
                {"passportNumber": "C12345678"},
            ]
        }
    }


class PassengerRead(PassengerBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Passenger ID.",
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "firstName": "Ada",
                    "lastName": "Lovelace",
                    "email": "ada@example.com",
                    "phone": "+1-212-555-0199",
                    "birthDate": "1815-12-10",
                    "passportNumber": "D12345678",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }