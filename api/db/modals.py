from typing import List
from sqlmodel import Field, Relationship, SQLModel # type: ignore
from uuid import uuid4, UUID
from datetime import datetime,timezone

class TimestampMixin(SQLModel):
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))


class UserBase(SQLModel):
    email:str = Field(unique=True,index=True)
    username :str
   

class Users(UserBase,TimestampMixin, table=True):
    id: UUID | None = Field(primary_key=True, index=True, default_factory=uuid4)
    password :str
    todos : List["Todo"] = Relationship(back_populates="owner")

class CreateUser(UserBase):
    password: str
    pass

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: UUID | None = None







class TodoBase(SQLModel):
    title:str = Field(nullable=False)
    complete:bool = Field(default=False)

class Todo(TodoBase,TimestampMixin, table=True):
       
       id: int | None = Field(default=None, primary_key=True,index=True)
     
       owner_id: UUID | None = Field(default=None, foreign_key="users.id", nullable=False)
       owner:Users = Relationship(back_populates="todos")

class CreateTodo(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass