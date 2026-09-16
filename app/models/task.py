from dataclasses import dataclass


@dataclass
class Task:
    id: str
    title: str
    description: str | None
    completed: bool
    user_id: str