import os

from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres"
)

engine = create_engine(DATABASE_URL, echo=True)
# echo=True to see the generated SQL queries in the terminal, only dev env!


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
