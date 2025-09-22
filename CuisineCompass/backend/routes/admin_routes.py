# in routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.auth.auth import get_current_user  # adjust the import as needed
from backend.models import User  # adjust the import as needed

router = APIRouter()

@router.get("/admin-only")
def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"secret": "admin-data"}
