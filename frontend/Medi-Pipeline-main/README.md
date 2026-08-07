# Medi Pipeline Dashboard

Production-ready React frontend for the Medi Pipeline FastAPI backend. The app uses Vite, JavaScript, Material UI, Axios, Recharts, and React Flow.

## Features

- Material UI enterprise dashboard layout.
- User selector populated from `GET /users`.
- Pipeline execution with loading and error states via `GET /candidate-set/{userId}`.
- Summary cards for user name, role, ceiling level, and entry point.
- Responsive timing cards for total time and each pipeline stage.
- Recharts funnel visualization for backend-provided funnel counts.
- Searchable and sortable candidate table with content dialog.
- React Flow DAG visualization using `hierarchy.nodes` and `hierarchy.edges`.
- Comparison mode for up to three users.
- Centralized API configuration in `src/services/api.js`.

## Requirements

- Node.js 18 or newer.
- A running FastAPI backend exposing:
  - `GET /users`
  - `GET /candidate-set/{userId}`

## Setup

```bash
npm install
```

Create an optional `.env` file if your backend is not running at `http://localhost:8000`:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```text
src/
  components/
    UserSelector.jsx
    PipelineButton.jsx
    SummaryCards.jsx
    FunnelChart.jsx
    TimingCards.jsx
    CandidateTable.jsx
    DAGView.jsx
    ComparisonView.jsx
    LoadingSpinner.jsx
  hooks/
    useUsers.js
  pages/
    Dashboard.jsx
  services/
    api.js
  utils/
    formatters.js
  App.jsx
  main.jsx
```

## API Configuration

All backend calls go through `src/services/api.js`. Update `VITE_API_BASE_URL` in your environment to point the dashboard at another FastAPI host. No endpoint URLs are hardcoded in components.

## Backend Contract

The UI consumes the API responses exactly as provided by the backend. It expects the candidate-set response to include `pipeline_timing`, `funnel`, `candidate_set`, and `hierarchy` objects/arrays as returned from `GET /candidate-set/{userId}`.
