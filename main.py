from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session
from database import init_db, get_session
from models import Room, Booking
from datetime import date, datetime

app = FastAPI(title="Сириус Аренда API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}

@app.post("/rooms", response_model=Room)
def create_room(room: Room, session: Session = Depends(get_session)):
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

@app.get("/rooms", response_model=list[Room])
def get_roooms(session: Session = Depends(get_session)):
    rooms = session.exec(select(Room)).all()
    return rooms

@app.get("/rooms/{id}", response_model=Room)
def get_room(id: int, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Пространство не найдено")
    return room

@app.put("/rooms/{id}", response_model=Room)
def update_room(id: int, room_data: Room, session: Session = Depends(get_session)):
    db_room = session.get(Room, id)
    if not db_room:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Пространство не найдено")
    
    db_room.name = room_data.name
    db_room.capacity = room_data.capacity
    db_room.equipment = room_data.equipment
    
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room

@app.delete("/rooms/{id}")
def delete_room(id: int, session: Session = Depends(get_session)):
    room = session.get(Room, id)
    if not room:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Пространство не найдено")
    
    session.delete(room)
    session.commit()
    return {"detail": "Пространство успешно удалено"}

@app.post("/bookings", response_model=Booking, status_code=201)
def create_booking(booking: Booking, session: Session = Depends(get_session)):

    room = session.get(Room, booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    

    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="Время начала должно быть меньше времени окончания")

    overlapping_bookings = session.exec(
        select(Booking).where(
            Booking.room_id == booking.room_id,
            Booking.status == "активно",
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time
        )
    ).first()
    
    if overlapping_bookings:
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
        
    bookings = session.exec(
        select(Booking).where(
            Booking.room_id == id,
            Booking.start_time >= datetime.combine(date, datetime.min.time()),
            Booking.start_time <= datetime.combine(date, datetime.max.time())
        )
    ).all()
    
    return bookings