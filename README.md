# Incident Engine

**Enterprise-Grade Incident Management System**

Incident Engine is a full-stack, high-performance monitoring and reporting platform. It bridges a robust **FastAPI** backend with a modern **Next.js** frontend, utilizing **PostgreSQL** for relational data integrity and **Elasticsearch** for fuzzy, high-speed full-text search.

---

## 🚀 Core Features

* **Real-time Dashboard:** Responsive UI built with Next.js App Router and Tailwind CSS.
* **Fuzzy Search:** Elasticsearch-powered search for high-speed incident retrieval.
* **OAuth2 Authentication:** Secure JWT-based authentication flow with password hashing.
* **Layered Architecture:** Backend follows a strict separation of concerns (Models → Schemas → API Routes).
* **Asynchronous I/O:** Fully async database operations using `SQLAlchemy` and `asyncpg` for maximum throughput.
* **Database Migrations:** Version-controlled schema management via `Alembic`.
* **Containerized Environment:** Fully Dockerized setup for consistent development and deployment.

---

## 🛠️ Technical Stack

### Backend
* **Framework:** FastAPI (Python 3.12+)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 (Async)
* **Migrations:** Alembic
* **Validation:** Pydantic v2
* **Security:** JWT, OAuth2, Passlib (Bcrypt)
* **Search Engine:** Elasticsearch 8.x

### Frontend
* **Framework:** Next.js 14 (App Router)
* **Language:** TypeScript
* **Styling:** Tailwind CSS
* **State Management:** React Hooks (useState, useEffect)
* **API Client:** Axios (with Interceptors for Auth)

---

## 📐 Architecture Overview

The system is designed with a **Layered Architecture** to ensure maintainability and scalability.

1.  **Presentation Layer (Next.js):** Communicates with the API via an Axios client. Handles client-side state and optimistic UI updates.
2.  **API Layer (FastAPI):** Exposes RESTful endpoints. Utilizes Dependency Injection for database sessions and user authentication.
3.  **Data Layer (Postgres + Elasticsearch):** Postgres serves as the "Source of Truth," while Elasticsearch handles read-heavy search operations.

---

## 🚦 Getting Started

### Prerequisites
* Docker & Docker Compose
* Node.js 18+
* Python 3.10+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/incident-engine.git](https://github.com/your-username/incident-engine.git)
    cd incident-engine
    ```

2.  **Environment Setup:**
    Create a `.env` file in the root directory:
    ```env
    POSTGRES_USER=rishi_admin
    POSTGRES_PASSWORD=secure_password
    POSTGRES_DB=incident_management
    POSTGRES_SERVER=localhost
    SECRET_KEY=your_super_secret_key
    ```

3.  **Launch Infrastructure:**
    ```bash
    docker-compose up -d
    ```

4.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    alembic upgrade head
    uvicorn app.main:app --reload
    ```

5.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 🧠 Developer Insights: Why this Stack?

* **Why FastAPI?** I chose FastAPI for its native support for asynchronous programming and automatic OpenAPI documentation. For a 5-year Python developer, its type-hinting integration with Pydantic makes the code self-documenting and extremely robust.
* **Why SQLAlchemy Async?** Standard blocking ORMs can become a bottleneck in I/O-heavy applications. Using `asyncpg` ensures the backend can handle thousands of concurrent requests without blocking the event loop.
* **Why Elasticsearch?** While Postgres supports basic text search, Elasticsearch provides superior relevance scoring and fuzzy matching, which is critical for an incident manager where users might search for partial error codes or misspelled titles.

---

## 👨‍💻 Author

**Rishi Kant**
* Senior Python Backend Developer
* Expertise in FastAPI, Data Engineering, and Layered Architectures.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
