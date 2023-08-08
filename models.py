from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base
import uuid


# class GUID(TypeDecorator):
#     """Platform-independent GUID type.
#     Uses PostgreSQL's UUID type, otherwise uses
#     CHAR(32), storing as stringified hex values.
#     """
#     impl = CHAR

#     def load_dialect_impl(self, dialect):
#         if dialect.name == 'postgresql':
#             return dialect.type_descriptor(UUID())
#         else:
#             return dialect.type_descriptor(CHAR(32))

#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         elif dialect.name == 'postgresql':
#             return str(value)
#         else:
#             if not isinstance(value, uuid.UUID):
#                 return "%.32x" % uuid.UUID(value).int
#             else:
#                 # hexstring
#                 return "%.32x" % value.int

#     def process_result_value(self, value, dialect):
#         if value is None:
#             return value
#         else:
#             if not isinstance(value, uuid.UUID):
#                 value = uuid.UUID(value)
#             return value
          

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")

    modify_date = Column(DateTime, nullable=True)

    voter = relationship('User', secondary=question_voter, backref='question_voters')



class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")

    modify_date = Column(DateTime, nullable=True)
    
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    place_id = Column(Integer, ForeignKey("place.id"), nullable=True)
    place = relationship("Place", backref="users")


class Place(Base):
    __tablename__ = "place"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    number = Column(String, nullable=False)


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey("place.id"))
    place = relationship("Place", backref="devices")

    auth_id = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="devices")