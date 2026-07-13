# ITAsset & Incident Management Portal — Starter Scaffold

This is the Phase 1 foundation: working auth (JWT) + asset CRUD, wired
frontend-to-backend. See the chat response for the full 6-phase roadmap
to keep building this out.

## Run the backend
```
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
copy .env.example .env       # Windows: copy, Mac/Linux: cp
# edit .env with your PostgreSQL connection string
python create_tables.py
python seed.py
uvicorn app.main:app --reload
```
Backend runs at http://localhost:8000 — interactive docs at http://localhost:8000/docs

## Run the frontend
```
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173

## Demo login
- Email: admin@itsm.com
- Password: Admin@123
