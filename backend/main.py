from sqlalchemy import create_engine
from models import Base

def init_db() -> None:
    engine = create_engine("sqlite:///db.sqlite", echo=True, future=True)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
