from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.models.user import User
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from src.crud import contact as crud_contact

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new contact for authenticated user."""
    return crud_contact.create_contact(db=db, contact=contact, user_id=current_user.id)

@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user contacts with optional filtering."""
    return crud_contact.get_user_contacts(
        db=db, 
        user_id=current_user.id,
        skip=skip, 
        limit=limit, 
        first_name=first_name, 
        last_name=last_name, 
        email=email
    )

@router.get("/birthdays/upcoming", response_model=List[ContactResponse])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contacts with birthdays in next 7 days."""
    return crud_contact.get_user_upcoming_birthdays(db=db, user_id=current_user.id)

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific contact by ID."""
    db_contact = crud_contact.get_user_contact(
        db=db, contact_id=contact_id, user_id=current_user.id
    )
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int, 
    contact_update: ContactUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update existing contact."""
    updated_contact = crud_contact.update_contact(
        db=db, contact_id=contact_id, contact_update=contact_update, user_id=current_user.id
    )
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete contact by ID."""
    success = crud_contact.delete_contact(
        db=db, contact_id=contact_id, user_id=current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}