from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, and_, extract
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactResponse

router = APIRouter(tags=['dates'])


@router.get("/", response_model=List[ContactResponse])
def show_dates(db: Session = Depends(get_db)):
    day_start = date.today().day
    day_end = (date.today()+timedelta(days=7)).day
    stmt = select(Contact).filter(
        and_(
            extract('day', Contact.birthdate).between(day_start, day_end),
            extract('month', Contact.birthdate) == date.today().month
        )
    )
    contacts = db.execute(stmt)
    return contacts.scalars().all()
