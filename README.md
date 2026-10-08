# Business Listings Dashboard

A full-stack dashboard that stores business listings in MySQL, exposes aggregated
data through a FastAPI backend, and visualises it with React charts.

```
Data (CSV) -> FastAPI bulk insert -> MySQL -> FastAPI stats APIs -> React + Recharts
```

## Tech Stack
- **Frontend:** React (Vite), Recharts
- **Backend:** FastAPI (Python), SQLAlchemy, PyMySQL
- **Database:** MySQL
- **Data collection:** requests + BeautifulSoup (scraper), Faker (sample data)

## Project Structure
```
business-dashboard/
├── backend/
│   ├── main.py            # FastAPI app and endpoints
│   ├── database.py        # DB connection
│   ├── models.py          # listing_master table
│   ├── requirements.txt
│   └── scraper/
│       ├── scraper.py     # polite scraper (robots.txt check, delays)
│       ├── mock_data.py   # sample data generator
│       └── load_to_api.py # uploads CSV to the bulk API
├── frontend/              # React dashboard
├── dump.sql               # MySQL dump
└── README.md
```

## Setup Instructions

### 1. Database
```sql
CREATE DATABASE business_db;
```
Either let the backend create the table on first start, or import the dump:
```bash
mysql -u root business_db < dump.sql
```
Edit the connection string in `backend/database.py` (or set `DATABASE_URL`)
to match your MySQL user and password.

### 2. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### 3. Load data (skip if you imported dump.sql)
```bash
cd backend/scraper
python mock_data.py
python load_to_api.py listings_mock.csv
```

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/listings/bulk` | Bulk insert listings into MySQL |
| GET | `/stats/city` | Business count per city |
| GET | `/stats/category` | Business count per category |
| GET | `/stats/source` | Business count per source |
| GET | `/stats/total` | Total number of listings |

## Data Collection Approach
- The scraper (`scraper.py`) is built to be polite: it checks `robots.txt`
  before every request, waits between requests, and identifies itself with a
  User-Agent. It skips any URL the site disallows and does not try to bypass
  blocking.
- **Sample data:** listings in the database labelled `source = "Sample Data"`
  are generated with the Faker library (`mock_data.py`). They are **not real
  businesses**. The assignment allows mock data when scraping is blocked.
- **Real scraped rows:** none. All rows in the database (500+) are sample data
  generated with Faker, because large directories restrict automated scraping.
  The scraper is included and can be pointed at a permitted site by updating
  its selectors.

## Frontend Note (Learning Disclosure)
I am new to frontend development and React. For the dashboard in `frontend/`,
I used online resources and an AI assistant to help write the code. I then went
through the code to understand how it works:
- `fetch` gets JSON data from the FastAPI endpoints.
- `useState` stores the data in the page.
- `useEffect` runs the fetch when the page loads.
- `BarCard` and `PieCard` are reusable components that draw Recharts charts.

## Challenges Faced
- **Scraping restrictions:** large directories (Google Maps, Justdial) restrict
  automated access in their terms, and HTML structure differs per site, so
  selectors must be written per site. I used a robots.txt-respecting scraper
  and sample data to reach the required volume.
- **MySQL authentication:** the connection failed with "Access denied" because
  the connection string contained a placeholder password. Fixed by matching
  the credentials of the local MySQL server.
- **Environment setup on macOS:** shell PATH issues and running commands from
  the wrong folder (uvicorn must run inside `backend/`) took time to debug.
- **CORS:** the React app (port 5173) needed CORS enabled in FastAPI to call
  the API (port 8000).
- **New to React:** learning how components, state and data fetching work was
  a challenge, which is why the frontend uses a simple structure.
