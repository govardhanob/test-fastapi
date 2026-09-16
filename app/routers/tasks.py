from fastapi import APIRouter, Depends, HTTPException
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from app.core.firebase import db
from app.dependencies.auth import get_current_user
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("")
def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["uid"]

    task_data = {
        "title": task.title,
        "description": task.description,
        "completed": False,
        "user_id": user_id,
        "created_at": SERVER_TIMESTAMP,
    }

    doc_ref = db.collection("tasks").document()

    doc_ref.set(task_data)

    return {
        "id": doc_ref.id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "user_id": user_id,
    }

@router.get("")
def get_tasks(
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["uid"]

    query = (
        db.collection("tasks")
        .where("user_id", "==", user_id)
    )

    docs = query.stream()

    tasks = []

    for doc in docs:
        data = doc.to_dict()

        tasks.append({
            "id": doc.id,
            **data,
        })

    return tasks

@router.get("/{task_id}")
def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    doc_ref = db.collection("tasks").document(task_id)

    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    data = doc.to_dict()

    if data["user_id"] != current_user["uid"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return {
        "id": doc.id,
        **data,
    }

@router.put("/{task_id}")
def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: dict = Depends(get_current_user),
):
    doc_ref = db.collection("tasks").document(task_id)

    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    data = doc.to_dict()

    if data["user_id"] != current_user["uid"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    update_data = task.model_dump(exclude_unset=True)

    doc_ref.update(update_data)

    updated_doc = doc_ref.get()

    return {
        "id": updated_doc.id,
        **updated_doc.to_dict(),
    }


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    doc_ref = db.collection("tasks").document(task_id)

    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    data = doc.to_dict()

    if data["user_id"] != current_user["uid"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    doc_ref.delete()

    return {
        "message": "Task deleted",
    }
