import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, MetaData, event, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    with_loader_criteria,
)
from sqlalchemy.sql.functions import current_timestamp

# カラム等の命名規則
name_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=name_convention)


class DBContext(Base):
    """これを継承してモデルを作成すること"""

    # 抽象ベースクラスであることの宣言
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=current_timestamp(),
        onupdate=func.now(),
    )


class BaseContextWithDeletedAt(DBContext):
    "論理削除対応のBaseContext"

    __abstract__ = True

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        server_default=None,
    )


@event.listens_for(Session, "do_orm_execute")
def _add_filter_deleted_at(execute_state: Any) -> None:
    """公開設定がTrueのみ取得する
    以下のようにすると、論理削除済のデータも含めて取得可能
    select(...).filter(...).execution_options(include_non_public=True).
    """
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                BaseContextWithDeletedAt,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            ),
        )
