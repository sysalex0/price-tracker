from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

from config.secrets import secrets
from model import ModelBase


def init_db():
    # when import this function, the below code will run
    ModelBase.Base.metadata.create_all(engine, checkfirst=True)


connection_string = f'postgresql+psycopg2://{secrets["DATABASE_USER"]}:{secrets["DATABASE_PASSWORD"]}@{secrets["DATABASE_HOST"]}:{secrets["DATABASE_PORT"]}/{secrets["DATABASE_NAME"]}'
print(f"connection_string: {connection_string}")
engine = create_engine(connection_string, future=True)

Session = ScopedSession(sessionmaker())
Session(bind=engine)
