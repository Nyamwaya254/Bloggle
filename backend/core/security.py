from datetime import datetime, timedelta, timezone


from jose import JWTError, jwt
from core.config import settings

def create_access_token(data:dict):
    '''Creating a jwt token'''
    to_encode =data.copy()
    expire = datetime.now(timezone.utc) +timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,algorithm= settings.ALGORITHM)
    return encoded_jwt