# Support Ticket CRM

Support Ticket CRM is a full-stack web application built as part of the Datastraw AI + Tech Intern assessment. The application enables support teams to manage customer support tickets efficiently through a clean dashboard and REST API.

## Features

- Create support tickets
- View all tickets in a dashboard
- Search tickets by ID, customer, email, subject, or description
- Filter tickets by status
- View complete ticket details
- Update ticket status
- Add notes to tickets

## Tech Stack

- **Backend:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML + Tailwind CSS (CDN) + Vanilla JavaScript

## Folder Structure

```
support-crm/
├── backend/
│   ├── main.py          # FastAPI app + all routes
│   ├── models.py        # SQLAlchemy models (Ticket, Note)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # DB connection/session setup
│   └── sample_data.py   # optional script to seed sample tickets
├── frontend/
│   ├── index.html       # dashboard (list, search, filter)
│   ├── create.html      # create ticket form
│   ├── ticket.html       # ticket details + status/notes
│   ├── 404.html
│   └── app.js            # shared JS helpers
├── database/
│   └── crm.db            # created automatically on first run
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run Locally

1. Clone the repo and go into the backend folder:
   ```
   cd support-crm/backend
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r ../requirements.txt
   ```

4. (Optional) Add sample tickets to try the UI with some data:
   ```
   python sample_data.py
   ```

5. Run the server:
   ```
   uvicorn main:app --reload
   ```

6. Open the app in your browser:
   ```
   http://127.0.0.1:8000
   ```

   The FastAPI backend also serves the frontend, so this same URL loads the dashboard.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tickets | Create a new ticket |
| GET | /api/tickets | List tickets (supports `?status=` and `?search=`) |
| GET | /api/tickets/{ticket_id} | Get full details of one ticket |
| PUT | /api/tickets/{ticket_id} | Update status and/or add a note |

## Deployment (Railway.app)

1. Push this project to a GitHub repository.
2. Go to [railway.app](https://railway.app) and create a new project from your GitHub repo.
3. Railway auto-detects Python. Set the start command to:
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
   (or `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` depending on root directory settings)
4. Add a build command if needed:
   ```
   pip install -r requirements.txt
   ```
5. Deploy. Railway will give a public URL once the build finishes.

## Notes

- Ticket IDs are auto-generated in the format `TKT-XXXX`.
- Status can only be `Open`, `In Progress`, or `Closed`.
- Closing a ticket asks for confirmation on the details page before the request is sent.
- Search works across ticket ID, customer name, email, subject, and description, and updates as you type (debounced).
