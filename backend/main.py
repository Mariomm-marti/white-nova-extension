from datetime import datetime
from os.path import exists
from time import sleep
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
    last_run = None
    while True:
        if not exists("./db.sqlite"):
            engine = init_db()
            last_run = None
        try:
            with Session(engine) as session:
                print(f"[siva:backend/sync_users] Operation started at '{datetime.now()}'")
                session.execute("PRAGMA foreign_keys = ON;")
                sync_users(session, last_run, 21, 22)
                session.commit()
                session.close()
                print(f"[siva:backend/sync_users] Operation finished correctly at '{datetime.now()}'")
                last_run = datetime.now()
        except Exception:
            print(f"[siva:backend/sync_users] Operation failed at '{datetime.now()}'")
            sleep(15)
            continue
        sleep(86400) # 86400s -> 1d
