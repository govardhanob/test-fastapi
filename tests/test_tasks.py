import unittest

from fastapi.encoders import jsonable_encoder
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from app.routers import tasks
from app.schemas.task import TaskCreate


class FakeDocument:
    id = "task-123"

    def __init__(self):
        self.saved_data = None

    def set(self, data):
        self.saved_data = data


class FakeCollection:
    def __init__(self):
        self.doc = FakeDocument()

    def document(self):
        return self.doc


class FakeDatabase:
    def __init__(self):
        self.tasks_collection = FakeCollection()

    def collection(self, name):
        if name != "tasks":
            raise AssertionError(f"Unexpected collection: {name}")
        return self.tasks_collection


class CreateTaskTest(unittest.TestCase):
    def test_create_task_response_is_json_serializable(self):
        fake_db = FakeDatabase()
        original_db = tasks.db
        tasks.db = fake_db

        try:
            response = tasks.create_task(
                TaskCreate(title="Write tests", description="Catch sentinel bug"),
                current_user={"uid": "user-123"},
            )
        finally:
            tasks.db = original_db

        self.assertEqual(
            fake_db.tasks_collection.doc.saved_data,
            {
                "title": "Write tests",
                "description": "Catch sentinel bug",
                "completed": False,
                "user_id": "user-123",
                "created_at": SERVER_TIMESTAMP,
            },
        )
        self.assertEqual(
            jsonable_encoder(response),
            {
                "id": "task-123",
                "title": "Write tests",
                "description": "Catch sentinel bug",
                "completed": False,
                "user_id": "user-123",
            },
        )


if __name__ == "__main__":
    unittest.main()
