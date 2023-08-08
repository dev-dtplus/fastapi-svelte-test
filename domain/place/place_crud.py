from datetime import datetime

from domain.place.place_schema import PlaceCreate
from models import Place, Device

from sqlalchemy import select
from sqlalchemy.orm import Session


def create_place(db: Session,
                  place_create: PlaceCreate):
    
    db_place = Place(name=place_create.name,
                      address=place_create.address,
                      number=place_create.number)
    db.add(db_place)
    db.commit()



def get_place(db: Session, 
                 place_id: int):
    
    place = db.query(Place).get(place_id)
    return place