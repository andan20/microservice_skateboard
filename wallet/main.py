from fastapi import FastAPI
from database.db import wait_for_db, SessionDep
from sqlmodel import select
from models.wallet import Wallet


app = FastAPI()

@app.on_event("startup")
def on_startup():
    wait_for_db()

@app.get("/")
async def root():
    return {"message": "Skateboad rental service"}



@app.get("/balance/{username}")
async def check_balance(username: str, session: SessionDep):
    username = username.lower()
    balance = session.exec(select(Wallet).where(Wallet.username == username)).all()
    return balance


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


@app.get("/health")
async def health_check():
    return {"status": "ok"}