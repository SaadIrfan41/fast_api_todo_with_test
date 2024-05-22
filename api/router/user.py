from typing import Any
from fastapi import APIRouter
from api.deps import CurrentUser, SessionDep
from api.core.security import get_password_hash
from api.db.modals import CreateUser, UserBase, Users


router = APIRouter()


@router.post("/create_user", response_model=Users)
def create_user(session: SessionDep, user: CreateUser):
    db_user = Users.model_validate(
        user, update={"password": get_password_hash(user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserBase)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user
