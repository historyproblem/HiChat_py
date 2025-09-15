from __future__ import annotations
from sqlalchemy import String, ForeignKey, Text, DateTime, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from DataBases import Base

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)

    messages: Mapped[list[MessagesOrm]] = relationship(back_populates="author", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_name_surname", "name", "surname"),
    )

class ChatsOrm(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    first_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    second_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    messages: Mapped[list[MessagesOrm]] = relationship(back_populates="chat", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("first_user_id", "second_user_id", name="uq_chat_pair"),
    )

class MessagesOrm(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # совместимость со старым подходом
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chat: Mapped[ChatsOrm] = relationship(back_populates="messages")
    author: Mapped[UsersOrm] = relationship(back_populates="messages")

    __table_args__ = (
        Index("ix_messages_chat_id_created", "chat_id", "created_at"),
    )
