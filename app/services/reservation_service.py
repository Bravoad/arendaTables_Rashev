from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate


def get_all_reservations(db: Session):
    """
    Возвращает список всех броней.
    """
    return db.query(Reservation).all()


def get_reservation_by_id(db: Session, reservation_id: int):
    """
    Возвращает бронь по её идентификатору.
    """
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


def create_reservation(db: Session, reservation_in: ReservationCreate):
    """
    Создаёт новую бронь для столика, проверяя на конфликт времени.
    Если временной интервал пересекается с существующей бронью,
    возбуждается исключение ValueError.
    """
    reservation_start = reservation_in.reservation_time
    reservation_end = reservation_start + timedelta(minutes=reservation_in.duration_minutes)

    existing_reservations = db.query(Reservation).filter(
        Reservation.table_id == reservation_in.table_id
    ).all()

    for existing in existing_reservations:
        existing_start = existing.reservation_time
        existing_end = existing_start + timedelta(minutes=existing.duration_minutes)
        if (reservation_start < existing_end) and (reservation_end > existing_start):
            raise ValueError("Столик уже зарезервирован на данный временной интервал")

    new_reservation = Reservation(**reservation_in.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


def delete_reservation(db: Session, reservation_id: int):
    """
    Удаляет бронь по идентификатору.
    Если бронь не найдена, возвращается None.
    """
    reservation = get_reservation_by_id(db, reservation_id)
    if not reservation:
        return None

    db.delete(reservation)
    db.commit()
    return reservation
