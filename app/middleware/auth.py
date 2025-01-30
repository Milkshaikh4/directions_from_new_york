from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def authenticate_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Middleware to check if a Bearer token is provided.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Unauthorized. Missing Bearer token.")

    # For now, accept any non-empty token
    return credentials.credentials
