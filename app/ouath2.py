import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.schemas import TokenData

def create_token(payload: dict):
    data = payload.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire_time})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credential_exception
    return token_data
