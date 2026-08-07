# Supra Engine Analytics

A FastAPI + React dashboard that computes a user's accessible clinical knowledge set using a graph-based permission pipeline.

The project traverses a healthcare knowledge graph using BFS from a user-specific entry point, injects Zone 2 nodes, applies five sequential permission checks, and visualizes the resulting candidate set.

---

## Features

- User-based pipeline execution
- Breadth First Search (BFS) graph traversal
- Permission compiler with O(1) lookups
- Zone 2 node injection
- Five sequential permission filters
- Candidate set generation
- Interactive dashboard
- Hierarchy (DAG) visualization
- Filter funnel visualization
- Pipeline timing metrics
- User comparison dashboard

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)

### Frontend
- React
- Vite
- Material UI
- Axios
- React Flow
- Recharts

---

## Project Structure

```
backend/
    app/
        api/
        models/
        schemas/
        services/
        main.py

frontend/
    Medi-Pipeline-main/
        src/
            components/
            hooks/
            pages/
            services/
```

---

## Setup

### 1. Clone repository

```bash
git clone <repository-url>
cd supra_engine
```

### 2. Backend

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r backend/requirements.txt
```

Create a `.env` file inside `backend`.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

Run the backend.

```bash
cd backend
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

### 3. Frontend

```bash
cd frontend/Medi-Pipeline-main
npm install
npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

## Database

The project uses PostgreSQL hosted on Supabase.

Database schema and sample data are available in

```
supabase/schema.sql
supabase/seed.sql
```

---

## Pipeline Overview

1. Resolve user entry point
2. Traverse hierarchy using BFS
3. Inject Zone 2 nodes
4. Apply five sequential permission checks
5. Generate candidate set
6. Return analytics and visualization data

---

## API Endpoints

### Get Users

```
GET /users
```

### Run Candidate Pipeline

```
GET /candidate-set/{user_id}
```

---

## Visualization

- Funnel Chart
- Hierarchy DAG
- Candidate Table
- Timing Cards
- Summary Cards
- Multi-user Comparison

---

## Environment Variables

```
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

Refer to `.env.example`.
