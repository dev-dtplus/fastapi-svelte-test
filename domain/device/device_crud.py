
from datetime import datetime

from sqlalchemy.orm import Session

from domain.device.device_schema import DeviceCreate
from models import Place, Device, User

from sqlalchemy import select





def create_device(db: Session,
                  place: Place):
                  #device_create: DeviceCreate
    
    db_device = Device(place=place)
    db.add(db_device)
    db.commit()


# def create_qrcode(db: Session):
#     return "qrcode"

async def get_device(db: Session, device_id: int):
    query = select(Device).filter(Device.id == device_id)
    #query = select(Device).get(device_id)
    db_device = await db.execute(query)
    db_device = db_device.scalars().first()

    return db_device

    #return db.query(Device).get(device_id)

# async def get_async_question_list(db: Session):
#     data = await db.execute(select(Question)
#                             .order_by(Question.create_date.desc())
#                             .limit(10))
#     return data.all()

async def get_device_and_state_by_auth_id(db: Session, auth_id: int):
    query = select(Device).filter(Device.auth_id == auth_id)
    db_device = await db.execute(query)
    db_device = db_device.scalars().first()
    #db_device = db.query(Device).filter(Device.auth_id == auth_id).first()
    user_id = None
    if db_device:
        #print(db_device.user_id)
        user_id = db_device.user_id

    return db_device, None#user_id


async def update_device_auth_id(db: Session,
                    db_device: Device,
                    auth_id: int):
    
    db_device.auth_id = auth_id
    db_device.user_id = None

    db.add(db_device)
    await db.commit()

async def update_device_auth_user(db: Session,
                    db_device: Device,
                    user: User):
    
    db_device.user_id = user.id
    db.add(db_device)
    await db.commit()