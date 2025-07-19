from fastapi import FastAPI
from database.db import wait_for_db, SessionDep
from sqlmodel import select
from models.rent import Rent
from datetime import datetime, UTC
import requests


app = FastAPI()

@app.on_event("startup")
def on_startup():
    wait_for_db()


@app.get("/info_rent/{username}")
async def get_info(username: str, session: SessionDep):
    info = session.exec(select(Rent).where(Rent.username == username)).first()
    return info


@app.get("/info_rent/{number}")
async def get_info(number: int, session: SessionDep):
    info = session.exec(select(Rent).where(Rent.number == number)).first()
    return info


@app.post("/new_rent/{username}")
async def new_rent(username: str, number: int, session: SessionDep):
    user_info = session.exec(select(Rent).where(Rent.username == username)).first()
    if user_info:
        return
    is_ban = requests.get(f"http://wallet:8002/ban/{username}").json()
    if is_ban:
        return
    is_skate_free = requests.get(f"http://skateboards:8001/is_free/{number}").json()
    if not is_skate_free:
        return


    rent = Rent(username=username, number=number, time_start = datetime.now(UTC))
    session.add(rent)
    session.commit()

    requests.post(f"http://skateboards:8001/add_rent/{number}")

    requests.post(f"http://wallet:8002/deletemoney/{username}?to_delete={100}")

    session.refresh(rent)
    return rent


@app.post("/delete_rent/{username}")
async def delete_rent(username: str, session: SessionDep):
    rent_info = session.exec(select(Rent).where(Rent.username == username)).first()
    if not rent_info:
        return

    num = rent_info.number
    session.delete(rent_info)

    requests.post(f"http://skateboards:8001/delete_rent/{num}")

    session.commit()
    return {"message": "succes"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}