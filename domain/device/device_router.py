from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from domain.device import device_schema, device_crud
from domain.place import place_schema, place_crud
from domain.user.user_router import get_current_user
from models import User
import time

import asyncio
from database import get_db, get_async_db

from starlette import status

import random

from sse_starlette.sse import EventSourceResponse
#from models import Question

router = APIRouter(
    prefix="/api/device",
)


# @router.post("/create/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
# def device_create(place_id: int, db: Session = Depends(get_db)):

#     place = place_crud.get_place(db, place_id=place_id)

#     if not place:
#         raise HTTPException(status_code=404, detail="Place not found")

#     device_crud.create_device(db=db,  place=place)#device_create=_device_create,



# @router.get("/qrcode/update/{device_id}")
# def device_qrcode_create(device_id:int, db: Session = Depends(get_db)):
#     device = device_crud.get_device(db, device_id=device_id)
#     if not device:
#         raise HTTPException(status_code=404, detail="Device not found")
    
#     auth_id = random.randint(100000, 999999)

#     device_crud.update_device_auth_id(db=db, db_device=device, auth_id=auth_id)

#     flags[str(auth_id)] = None

#     return {"auth_id":str(auth_id)}




# flags = {}

# MESSAGE_STREAM_DELAY = 1
# MESSAGE_STREAM_RETRY_TIMEOUT = 15000



# @router.get('/qrcode/checkstream/{auth_id}')
# async def message_stream(auth_id:int, request: Request):
#     def valid_auth_id():
#         return flags.get(str(auth_id)) is not None
        
#     async def event_generator():
#         while True:
#             # If client was closed the connection
#             if await request.is_disconnected():
#                 break

#             # Checks for new messages and return them to client if any
#             if valid_auth_id():
#                 yield {
#                         "event": "auth success",
#                         "id": "auth_id",
#                         "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
#                         "data": "message_content"
#                 }
#                 break

#             await asyncio.sleep(1)#MESSAGE_STREAM_DELAY

#     return EventSourceResponse(event_generator())


# @router.get("/qrcode/auth/{auth_id}")
# async def device_qrcode_auth(auth_id: int,db: Session = Depends(get_async_db), current_user: User = Depends(get_current_user)):
#     device, _ = await device_crud.get_device_and_state_by_auth_id(db, auth_id=auth_id)

#     if not device:
#         raise HTTPException(status_code=404, detail="Auth session not found")
    
#     flags[str(auth_id)] = current_user.id

#     await device_crud.update_device_auth_user(db=db, db_device=device, user=current_user)
#     return {"user":"authenticated"}