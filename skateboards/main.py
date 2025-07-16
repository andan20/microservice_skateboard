from fastapi import FastAPI
from database.db import wait_for_db, SessionDep
from sqlmodel import select
from models.skateboards import Skateboards


app = FastAPI()

@app.on_event("startup")
def on_startup():
    wait_for_db()


@app.get("/info/{number}")
async def get_info(number: int, session: SessionDep):
    skate = session.exec(select(Skateboards).where(Skateboards.number == number)).first()
    return skate


@app.get("/is_free/{number}")
async def get_info(number: int, session: SessionDep):
    skate = session.exec(select(Skateboards).where(Skateboards.number == number)).first()
    return skate.is_free


@app.post("/add_rent/{number}")
async def new_rent(number: int, session: SessionDep):
    skate = session.exec(select(Skateboards).where(Skateboards.number == number)).first()
    if not skate:
        return

    skate.is_free = False

    session.commit()
    session.refresh(skate)
    return skate


@app.post("/delete_rent/{number}")
async def del_rent(number: int, session: SessionDep):
    skate = session.exec(select(Skateboards).where(Skateboards.number == number)).first()
    if not skate:
        return

    skate.is_free = True

    session.commit()
    session.refresh(skate)
    return skate


@app.post("/add_skateboard/{number}")
async def new_skate(number: int, session: SessionDep, model: str | None = None,
                    color: str | None = None, num_of_automat: int | None = None):
    skate = session.exec(select(Skateboards).where(Skateboards.number == number)).first()
    if skate:
        return

    skate = Skateboards(number = number, model = model, color = color,
                        is_free = True, num_of_automat = num_of_automat)
    session.add(skate)
    session.commit()
    session.refresh(skate)
    return skate




@app.get("/health")
async def health_check():
    return {"status": "ok"}