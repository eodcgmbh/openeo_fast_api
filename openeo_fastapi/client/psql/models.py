import datetime
import uuid
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import BOOLEAN, VARCHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM, JSON, UUID

from openeo_fastapi.client.psql.settings import BASE


class Status(Enum):
    created = "created"
    queued = "queued"
    running = "running"
    canceled = "canceled"
    finished = "finished"
    error = "error"


class UserORM(BASE):
    """ORM for the user table."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    oidc_sub = Column(VARCHAR, unique=True)
    created_at = Column(
        DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
    )


class JobORM(BASE):
    """ORM for the job table."""

    __tablename__ = "jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True)
    process_graph_id = Column(VARCHAR, nullable=False)
    status = Column(ENUM(Status), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created = Column(
        DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    synchronous = Column(BOOLEAN, default=False, nullable=False)  # if null assume False


class ProcessGraph(BaseModel):
    process_graph_id: str
    process_graph: dict
    user_id: uuid.UUID
    created: datetime.datetime

    def get_orm(self):
        return ProcessGraphORM

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        extra = "ignore"


class ProcessGraphORM(BASE):
    """ORM for the process graph table."""

    __tablename__ = "process_graph"

    process_graph_id = Column(VARCHAR, primary_key=True)
    process_graph = Column(JSON, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    created = Column(
        DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
    )


class UdpORM(BASE):
    """ORM for the UDPS table."""

    __tablename__ = "udps"

    udp_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    process_graph = Column(JSON, nullable=False)
    created = Column(
        DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    parameters = Column("parameters", JSON)
    returns = Column("returns", JSON)
    summary = Column("summary", String)
    description = Column("description", String)
