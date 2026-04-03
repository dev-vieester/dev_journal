from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()")
    )

class JournalEntries(Base):
    __tablename__ = "journalentries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("now()")
    )

    owner = relationship("User")
    snippets = relationship("CodeSnippets", cascade="all, delete-orphan")

class CodeSnippets(Base):
    __tablename__ = "codesnippets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=True)
    entry_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("journalentries.id", ondelete="CASCADE"), nullable=False
    )

    entry = relationship("JournalEntries")
