import random
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from pathlib import Path

from backend import models, schemas
from backend.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support Ticket CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_ticket_id():
    """Creates a ticket id like TKT-4821"""
    number = random.randint(1000, 9999)
    return f"TKT-{number}"


@app.get("/api/health")
def health():
    return {"message": "Support Ticket CRM API is running"}


@app.post("/api/tickets", response_model=schemas.TicketDetailOut, status_code=201)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    new_id = generate_ticket_id()
    while db.query(models.Ticket).filter(models.Ticket.ticket_id == new_id).first():
        new_id = generate_ticket_id()

    db_ticket = models.Ticket(
        ticket_id=new_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open",
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.get("/api/tickets", response_model=list[schemas.TicketListOut])
def get_tickets(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Ticket)

    if status and status != "All":
        query = query.filter(models.Ticket.status == status)

    if search:
        search_text = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.ticket_id.ilike(search_text),
                models.Ticket.customer_name.ilike(search_text),
                models.Ticket.customer_email.ilike(search_text),
                models.Ticket.subject.ilike(search_text),
                models.Ticket.description.ilike(search_text),
            )
        )

    tickets = query.order_by(models.Ticket.created_at.desc()).all()
    return tickets

@app.get("/api/tickets/{ticket_id}", response_model=schemas.TicketDetailOut)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.put("/api/tickets/{ticket_id}", response_model=schemas.TicketDetailOut)
def update_ticket(ticket_id: str, update: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    valid_statuses = ["Open", "In Progress", "Closed"]

    if update.status:
        if update.status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status value")
        ticket.status = update.status

    if update.note_text:
        new_note = models.Note(ticket_id=ticket.id, note_text=update.note_text)
        db.add(new_note)

    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)
    return ticket

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
