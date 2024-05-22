from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from api.deps import CurrentUser, SessionDep
from api.db.modals import CreateTodo, Todo, TodoUpdate
from typing import List, Sequence
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()

def TodoNotFoundError():
    return HTTPException(status_code=404, detail="Todo not found")

@router.get("/todos",response_model=List[Todo])
async def read_all_todos(db: SessionDep,currentUser: CurrentUser,skip: int = 0, limit: int = 10 ) -> Sequence[Todo]:
     """
    Get Todos with pagination from the database.

    Args:
        db (Session): The database session.
        currentUser (CurrentUser): The current logged in user.
        offset (int): The number of items to skip.
        per_page (int): The number of items per page.

    Returns:
        List[Todo]: The list of Todos.
    """
     todos = db.exec(select(Todo).where(Todo.owner_id == currentUser.id).offset(skip).limit(limit)).all()
     return todos

@router.get("/todos/{id}",response_model=List[Todo])
async def read_single_todo(db: SessionDep,currentUser: CurrentUser,todo_id:int) ->Todo:
     """
    Get Todos with pagination from the database.

    Args:
        db (Session): The database session.
        currentUser (CurrentUser): The current logged in user.
        todo_id (int): The id of the Todo item to retrieve.

    Returns:
        Todo: The retrieved Todo.
    """
     todo = db.exec(select(Todo).where(Todo.owner_id == currentUser.id, Todo.id == todo_id)).first()
     if todo is None:
            raise TodoNotFoundError()
     return todo



@router.post("/create_todo",response_model=Todo)
async def create_todo(
    todo: CreateTodo,
    currentUser: CurrentUser,
    db: SessionDep,
)-> Todo:
    """
    Create a new Todo in the database.

    Args:
        todo (CreateTodo): The Todo item to be created.
        currentUser (CurrentUser): The current logged in user.
        db (Session): The database session.

    Returns:
        Todo: The created Todo item.
    """
    try:
         new_todo = Todo.model_validate(todo,update={"owner_id":currentUser.id})
         db.add(new_todo)
         db.commit()
         db.refresh(new_todo)
    
    except SQLAlchemyError as e:
         db.rollback()
         print(f"Error creating a TODO : {e}")
         raise
    
    return new_todo


@router.put("/todos/{id}",response_model=Todo)
async def update_todo(
    todo: TodoUpdate,
    currentUser: CurrentUser,
    db: SessionDep,
    todo_id: int
)-> Todo:
    """
    Update an existing Todo in the database.

    Args:
        todo (TodoUpdate): The Todo to Update.
        currentUser (CurrentUser): The current logged in user.
        db (Session): The database session.
        todo_id (int): The ID of the Todo to update.

    Returns:
        Todo: The updated Todo.
    """
    try:
         db_todo=db.get(Todo, todo_id)
         if db_todo is None:
            raise TodoNotFoundError()
         if db_todo.owner_id != currentUser.id:
            raise HTTPException(status_code=403, detail="Permission Denied")
         todo_data = todo.model_dump(exclude_unset=True)
         todo_data["updated_at"] = datetime.now()
         for key, value in todo_data.items():
               setattr(db_todo, key, value)
         db.add(db_todo)
         db.commit()
         db.refresh(db_todo)
         
    except SQLAlchemyError as e:
         db.rollback()
         print(f"Error Updating a TODO : {e}")
         raise
    
    return db_todo  