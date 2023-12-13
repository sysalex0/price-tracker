from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

from model import ModelBase


def init_db():
    # when import this function, the below code will run
    ModelBase.Base.metadata.create_all(engine, checkfirst=True)


secrets = dotenv_values(".env")
connection_string = f'postgresql+psycopg2://{secrets["DATABASE_USER"]}:{secrets["DATABASE_PASSWORD"]}@{secrets["DATABASE_HOST"]}:{secrets["DATABASE_PORT"]}/{secrets["DATABASE_NAME"]}'
engine = create_engine(connection_string, echo=True, future=True)

Session = ScopedSession(sessionmaker())
Session(bind=engine)
