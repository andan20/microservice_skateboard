from fastapi import FastAPI
from database.db import wait_for_db, SessionDep
from sqlmodel import select
from models.wallet import Wallet


app = FastAPI()

@app.on_event("startup")
def on_startup():
    wait_for_db()



@app.get("/info/{username}")
async def get_info(username: str, session: SessionDep):
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    return user

@app.get("/balance/{username}")
async def check_balance(username: str, session: SessionDep):
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    return user.balance

@app.get("/ban/{username}")
async def is_user_ban(username: str, session: SessionDep):
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    return user.is_ban


@app.post("/register/{username}")
async def new_user(username: str, balance: int, session: SessionDep):
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    if user:
        return
    if balance < 0 or balance > 1e9:
        return

    wallet = Wallet(username=username, balance=balance)
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet


@app.post("/addmoney/{username}")
async def add_money(username: str, to_add: int, session: SessionDep):
    if to_add < 0 or to_add > 1e9:
        return
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    if not user:
        return

    if user.balance + to_add > 1e9:
        return

    user.balance += to_add
    session.commit()
    session.refresh(user)
    return user


@app.post("/deletemoney/{username}")
async def add_money(username: str, to_delete: int, session: SessionDep):
    if to_delete < 0 or to_delete > 1e9:
        return
    username = username.lower()
    user = session.exec(select(Wallet).where(Wallet.username == username)).first()
    if not user:
        return

    if user.balance - to_delete < 0:
        user.is_ban = True

    else:
        user.balance -= to_delete

    session.commit()
    session.refresh(user)
    return user

@app.get("/health")
async def health_check():
    return {"status": "ok"}