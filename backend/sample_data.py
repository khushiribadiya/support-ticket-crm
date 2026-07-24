from backend import models, schemas
from backend.database import SessionLocal

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

sample_tickets = [
    {
        "ticket_id": "TKT-1001",
        "customer_name": "Rahul Sharma",
        "customer_email": "rahul.sharma@example.com",
        "subject": "Order not delivered yet",
        "description": "My order was supposed to arrive 3 days ago but tracking shows no update.",
        "status": "Open",
    },
    {
        "ticket_id": "TKT-1002",
        "customer_name": "Priya Verma",
        "customer_email": "priya.verma@example.com",
        "subject": "Refund not processed",
        "description": "I returned the product a week ago but the refund has not reflected in my account.",
        "status": "In Progress",
    },
    {
        "ticket_id": "TKT-1003",
        "customer_name": "Amit Kulkarni",
        "customer_email": "amit.k@example.com",
        "subject": "Wrong item received",
        "description": "I ordered a blue shirt but received a red one instead.",
        "status": "Closed",
    },
]

for data in sample_tickets:
    existing = db.query(models.Ticket).filter(models.Ticket.ticket_id == data["ticket_id"]).first()
    if not existing:
        ticket = models.Ticket(**data)
        db.add(ticket)

db.commit()
db.close()

print("Sample tickets added successfully.")
