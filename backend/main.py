from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from models import Base
from services import sync_users

@compiles(Insert)
def insert_skip_unique(insert, compiler, **kw):
    return compiler.visit_insert(insert.prefix_with("OR IGNORE"), **kw)

def init_db() -> Engine:
    engine = create_engine("sqlite:///db.sqlite", future=True)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    engine = init_db()
    with Session(engine) as session:
        sync_users(session, datetime(2022, 8, 10), 21, 22)
        session.commit()
