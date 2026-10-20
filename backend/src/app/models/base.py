from sqlalchemy.orm import DeclarativeBase


# this is needed to support sqlalchemy migration generations
# from python entities
class Base(DeclarativeBase):
    pass
