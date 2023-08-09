from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from domain.device import device_schema, device_crud
from domain.place import place_schema, place_crud
from domain.user.user_router import get_current_user
from models import User
import time

import asyncio
from database import get_db, get_async_db, async_engine, akv_db
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

import random

#from sse_starlette.sse import EventSourceResponse
#from models import Question

router = APIRouter(
    prefix="/api/device",
)


@router.post("/create/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def device_create(place_id: int, db: Session = Depends(get_db)):

    place = place_crud.get_place(db, place_id=place_id)

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    device_crud.create_device(db=db,  place=place)#device_create=_device_create,



@router.get("/qrcode/update/{device_id}")
async def device_qrcode_create(device_id:int, db: Session = Depends(get_async_db)):
    device = await device_crud.get_device(db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    auth_id = random.randint(100000, 999999)

    await device_crud.update_device_auth_id(db=db, db_device=device, auth_id=auth_id)

    #flags[str(auth_id)] = None

    return {"auth_id":str(auth_id)}



@router.get("/qrcode/auth/{auth_id}")
async def device_qrcode_auth(auth_id: int,db: Session = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    device = await device_crud.get_device_by_auth_id(db, auth_id=auth_id)

    if not device:
        raise HTTPException(status_code=404, detail="Auth session not found")
    
    akv_db.set_default(str(auth_id), str(current_user.id))

    #flags[str(auth_id)] = current_user.id

    await device_crud.update_device_auth_user(db=db, db_device=device, user=current_user)
    return {"user":"authenticated"}




@router.get('/qrcode/longpolling/{auth_id}')
async def longpolling(auth_id:int):
    user_id = None

    while True:
        user_id = akv_db.get(str(auth_id))
        if user_id is not None:
            break
        await asyncio.sleep(1)

    akv_db.remove(str(auth_id))
    return {"user_id":user_id}