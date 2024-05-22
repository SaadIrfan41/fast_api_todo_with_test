
from collections.abc import Generator
from sqlmodel import  create_engine,Session,SQLModel

from api.settings import DATABASE_URL




connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)



# engine = create_engine(connection_string,echo=True)
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300,echo=True
)
# SQLModel.metadata.create_all(engine)



# def get_db():
#     db = Session(engine)
#     try:
#         yield db
#     finally:
#         db.close()

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)