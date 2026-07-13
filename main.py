from datetime import datetime, date
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import select, Session
from database import init_db, get_session
from models import Room, Booking

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  
    yield

app = FastAPI(title="Сириус Аренда API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Сервер Сириус.Аренда успешно запущен"}



@app.post("/rooms", response_model=Room, status_code=201)
def create_room(room: Room, session: Session = Depends(get_session)):
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
@app.get("/rooms", response_model=list[Room])
def get_rooms(session: Session = Depends(get_session)):
    return session.exec(select(Room)).all()

@app.get("/rooms/{id}", response_model=Room)
def get_room(id: int, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    return room

@app.put("/rooms/{id}", response_model=Room)
def update_room(id: int, updated_room: Room, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    room.name = updated_room.name
    room.capacity = updated_room.capacity
    room.equipment = updated_room.equipment
    
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

@app.delete("/rooms/{id}")
def delete_room(id: int, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    session.delete(room)
    session.commit()
    return {"detail": f"Комната {id} успешно удалена"}


@app.post("/bookings", response_model=Booking, status_code=201)
def create_booking(booking: Booking, session: Session = Depends(get_session)):
    # Защита: преобразуем строковые ISO-даты из JSON в Python datetime объекты
    if isinstance(booking.start_time, str):
        booking.start_time = datetime.fromisoformat(booking.start_time)
    if isinstance(booking.end_time, str):
        booking.end_time = datetime.fromisoformat(booking.end_time)

    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="Время начала не может быть позже времени окончания")

    room = session.get(Room, booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Указанная комната не существует")

    overlapping = session.exec(
        select(Booking).where(
            Booking.room_id == booking.room_id,
            Booking.status == "активно",
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time
        )
    ).first()
    
    if overlapping:
        raise HTTPException(status_code=409, detail="Это время в комнате уже забронировано")
        
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

@app.delete("/bookings/{id}")
def cancel_booking(id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    booking.status = "отменено"
    session.add(booking)
    session.commit()
    return {"detail": "Бронирование успешно отменено"}

@app.get("/rooms/{id}/bookings", response_model=list[Booking])
def get_room_bookings(id: int, date: date, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
        
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    bookings = session.exec(
        select(Booking).where(
            Booking.room_id == id,
            Booking.status == "активно",
            Booking.start_time <= end_of_day,
            Booking.end_time >= start_of_day
        )
    ).all()
    return bookings
