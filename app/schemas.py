from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import List


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr


class UserResponse(User):
    id: int
    created_at: datetime

class UserCreate(User):
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    id: int

class Entry(BaseModel):
    title: str
    body: str


class CreateEntry(Entry):
    pass

class CreateSnippet(BaseModel):
    language: str
    code: str

class SnippetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    language: str
    code: str
    entry_id: int

class EntryOut(Entry):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    created_at: datetime
    snippets: List[SnippetOut] = []

