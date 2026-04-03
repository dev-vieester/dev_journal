from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import CodeSnippets, JournalEntries, User
from app.schemas import CreateSnippet, SnippetOut


router = APIRouter(prefix="/snippets", tags=["Snippets"])


@router.post("/{entry_id}", response_model=SnippetOut, status_code=status.HTTP_201_CREATED)
def create_snippet(
    entry_id: int,
    snippet: CreateSnippet,
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

    snippet_data = snippet.model_dump()
    snippet_data["entry_id"] = entry_id
    new_snippet = CodeSnippets(**snippet_data)
    db.add(new_snippet)
    db.commit()
    db.refresh(new_snippet)
    return new_snippet
