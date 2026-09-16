from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "uid": current_user["uid"],
        "email": current_user.get("email"),
    }