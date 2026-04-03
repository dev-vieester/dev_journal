from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")