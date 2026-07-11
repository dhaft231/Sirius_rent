from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, JSON

class RoomBase(SQLModel):
    name: str = Field(index = True)
    capacity: int
    equipment: List[str] = Field(default=[], sa_type=JSON)

class Room(RoomBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class BookingBase(SQLModel):
    room_id: int = Field(foreign_key="room.id")
    start_time: datetime
    end_time: datetime
    user_name: str
    status: str = Field(default="активно")
    
class Booking(BookingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
