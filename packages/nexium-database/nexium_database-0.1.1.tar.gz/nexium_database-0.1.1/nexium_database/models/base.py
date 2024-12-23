from datetime import datetime, UTC
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)
    is_deleted: bool = Field(default=False, nullable=False)
