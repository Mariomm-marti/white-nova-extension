from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, Location, EventUser
from datetime import datetime
from intra import ic

def sync_users(session: Session, from_date: datetime, cursus_id: int, campus_id: int) -> None:
    """
    sync_users
    Using `from_date` as last sync date, takes all new cursuses and pushes all
    users into the database instance.
    If no `from_date` is provided (None), all users will be inserted.
    """
    if from_date is None:
        from_date = datetime(1970, 1, 1)
    params = {
            "filter[campus_id]": campus_id,
            "flter[blackhole]": False,
            "range[created_at]": f"{from_date},{datetime.now()}"
            }
    cursus_users = ic.pages_threaded(f"cursus/{cursus_id}/cursus_users", params=params)
    users = []
    for cursus_user in cursus_users:
        users.append(User(
                id = cursus_user["user"]["id"],
                login = cursus_user["user"]["login"]
                ))
    session.add_all(users)

def sync_users_locations(session: Session, from_date: datetime) -> None:
    """
    sync_locations
    Using `from_date` as last sync date, takes all new locations and pushes them
    to the database instance.
    If no `from_date` is provided (None), all locations will be inserted.
    Only the users registered on the DB will be looked up.
    """
    raw_query = select(User).where(User.last_search <= datetime.now() - from_date)
    result = session.execute(raw_query)
    for user in result.scalars():
        print(user)

def sync_events_users(from_date: datetime) -> None:
    pass
