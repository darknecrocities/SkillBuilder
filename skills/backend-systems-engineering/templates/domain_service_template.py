from typing import Protocol, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Project:
    id: str
    name: str
    owner_id: str
    created_at: datetime


class ProjectRepository(Protocol):
    def get_by_name_and_owner(self, name: str, owner_id: str) -> Optional[Project]:
        ...

    def save(self, project: Project) -> Project:
        ...


class DuplicateProjectException(Exception):
    def __init__(self, name: str):
        super().__init__(f"A project with name '{name}' already exists for this owner.")


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, name: str, owner_id: str) -> Project:
        existing = self.repo.get_by_name_and_owner(name, owner_id)
        if existing:
            raise DuplicateProjectException(name)

        project = Project(
            id=f"proj_{int(datetime.utcnow().timestamp())}",
            name=name.strip(),
            owner_id=owner_id,
            created_at=datetime.utcnow(),
        )
        return self.repo.save(project)
