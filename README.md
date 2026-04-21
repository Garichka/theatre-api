# theatre-api 🎭

## 📝 Description
**theatre-api** is a RESTful API service designed to automate theater operations. It allows users to browse the repertoire, check performance schedules, and book specific seats in real-time. The system includes a robust admin interface and strict validation to prevent double-booking.

---

## 🎯 Features
- **User Authentication:** Secure JWT-based login and registration.
- **Dynamic Repertoire:** Manage plays, actors, and genres.
- **Real-time Scheduling:** Track performances in different halls.
- **Smart Booking:** Choose specific rows and seats with automatic availability checks.
- **Admin Dashboard:** Full CRUD operations for theater staff.
- **Documentation:** Built-in Swagger and ReDoc UI.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/user/register/` | Register a new user |
| `POST` | `/api/user/token/` | Get JWT access/refresh tokens |
| `GET` | `/api/theatre/plays/` | List all plays (filterable by genre/actor) |
| `GET` | `/api/theatre/performances/` | View current performance schedule |
| `POST` | `/api/theatre/reservations/` | Create a new ticket reservation |
| `GET` | `/api/theatre/reservations/` | View your personal booking history |

---

## 🏗 Database Structure
The project uses **SQLite** for local development (simple setup) and is ready for **PostgreSQL** in production.
- **Play, Performance, TheatreHall:** Core business logic.
- **Ticket & Reservation:** Handling the sales flow.
- **Actor & Genre:** Supporting metadata.

---

## 🔑 Environment Variables
To run this project, you will need to add the following variables to your `.env` file:
`SECRET_KEY` — Your Django secret key.
`DEBUG` — Set to `True` for development, `False` for production.
`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` — Database credentials (if using PostgreSQL).

---

## 🐳 Docker
To run the application using Docker:
1. Ensure you have Docker installed.
2. Run the following command in the root directory:
```bash
docker-compose up --build
