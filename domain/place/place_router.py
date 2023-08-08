from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.device import device_schema, device_crud
from domain.place import place_schema, place_crud
#from domain.device.device_router import get_current_user
from models import User

from database import get_db, get_async_db

from starlette import status
#from models import Question

router = APIRouter(
    prefix="/api/place",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def place_create(_place_create: place_schema.PlaceCreate,
                    db: Session = Depends(get_db)):
    
    place_crud.create_place(db=db, place_create=_place_create)