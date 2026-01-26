# redschem docs

This guide explains how to run the redschem backend and frontend locally.

Before you start, make sure you have:

* Python 3.10+ installed
* Bun installed (for the frontend)
* A local PostgreSQL database running

---

## Prerequisites: PostgreSQL

redschem requires a PostgreSQL database. You must start one locally before running either the backend or the frontend.

If you already have Postgres installed:

1. Start the Postgres service
2. Create a new database (for example: `redschem`)
3. Create a user and password (or reuse your own)

Example (psql):

```sql
CREATE DATABASE redschem;
CREATE USER redschem_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE redschem TO redschem_user;
```

You will use this database URL in the `.env` files for both backend and frontend.

---

## Running the Backend

1. Open a terminal
2. `cd` into the backend directory:

```bash
cd be
```

3. Copy the example environment file and edit it:

```bash
cp .env.example .env
```

4. Open `.env` and fill in your credentials:

* PostgreSQL connection URL
* Any required secrets or tokens

5. Install Python dependencies (if not already installed):

```bash
pip install -r requirements.txt
```

6. Run the backend:

```bash
python .
```

If everything is configured correctly, the backend should connect to PostgreSQL and start without errors.

---

## Running the Frontend

The frontend is a SvelteKit application.

1. Open a new terminal
2. `cd` into the frontend directory:

```bash
cd fe
```

3. Copy the example environment file and edit it:

```bash
cp .env.example .env
```

4. Open `.env` and set your PostgreSQL database URL:

* Use the same database credentials you used for the backend

5. Install frontend dependencies:

```bash
bun install
```

6. Start the development server:

```bash
bun run dev
```

Open the printed local URL in your browser to access the frontend.

---

## Common Problems

* **Database connection failed**

  * Make sure PostgreSQL is running
  * Check that your database URL, username, and password are correct

* **Backend starts but frontend shows no data**

  * Make sure both backend and frontend are pointing to the same database

---

## Notes

* The backend must be running for the frontend to work properly
* Do not expose your `.env` files or database credentials publicly

