from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import  create_engine,Session,SQLModel

from api.settings import DATABASE_URL_TEST

connection_string = str(DATABASE_URL_TEST).replace(
    "postgresql", "postgresql+psycopg"
)

test_engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300,echo=True
)

def get_test_db() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session

SessionTestDep = Annotated[Session, Depends(get_test_db)]
def create_test_tables():
    print("Creating tables for testing..")
    SQLModel.metadata.create_all(test_engine)
    return ("Tables created..")

def drop_test_tables():
    print("Dropping tables..")
    SQLModel.metadata.drop_all(test_engine)
    return ("Tables dropped..")