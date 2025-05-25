from fastapi import FastAPI, Query, HTTPException
from sqlmodel import SQLModel, select
from app.models import Hero, HeroUpdate
from app.database import engine, SessionDep
from typing import Annotated

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Creating a Hero User
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Returning all Heros
@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Getting a Single Hero
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Updating a Hero
@app.put("/heroes/{hero_id}")
def update_hero(hero_id: int, hero_update: HeroUpdate, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Deleting a Hero
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
