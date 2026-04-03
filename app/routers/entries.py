from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import JournalEntries, User
from app.schemas import CreateEntry, EntryOut


router = APIRouter(prefix="/entries")

@router.post("", response_model=EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(
    content: CreateEntry,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content_data = content.model_dump()
    content_data["owner_id"] = current_user.id
    entry = JournalEntries(**content_data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("", response_model=List[EntryOut])
def get_entries(
    search_journal: str = "",
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = (
        db.query(JournalEntries)
        .filter(
            JournalEntries.owner_id == current_user.id,
            JournalEntries.title.contains(search_journal),
        )
        .limit(limit)
        .offset(offset)
        .all()
    )
    return entries

@router.get("/{entry_id}", response_model=EntryOut)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(JournalEntries)
        .filter(
            JournalEntries.id == entry_id,
            JournalEntries.owner_id == current_user.id,
        )
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    return entry

@router.put("/{entry_id}", response_model=EntryOut)
def update_entry(
    entry_id: int,
    content: CreateEntry,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(JournalEntries)
        .filter(
            JournalEntries.id == entry_id,
            JournalEntries.owner_id == current_user.id,
        )
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )

    update_data = content.model_dump()
    for field, value in update_data.items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(JournalEntries)
        .filter(
            JournalEntries.id == entry_id,
            JournalEntries.owner_id == current_user.id,
        )
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )

    db.delete(entry)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
