# Internet Usage Monitoring Service

## Description

A FastAPI-based service to monitor and analyze internet usage for different users.  
Includes APIs for analytics and a simple HTML frontend for user search.

## Setup Instructions

1. **Clone the repository** and enter the folder.
2. **Create a virtual environment** and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
   *(If you don’t have a requirements.txt, you can create one with: `pip freeze > requirements.txt`)*

4. **Create the database:**
   ```
   python create_db.py
   ```

5. **Ingest the data:**
   ```
   python ingest_data.py
   ```

6. **Run the server:**
   ```
   uvicorn main:app --reload
   ```

## API Usage

- **GET /** — Health check
- **GET /top-users** — Paginated top users by usage
- **GET /user-details?name=USERNAME&timestamp=YYYY-MM-DD%20HH:MM** — User usage by name and timestamp

## HTML Search Page

- Visit [http://127.0.0.1:8000/static/user_search.html](http://127.0.0.1:8000/static/user_search.html) for a simple user search interface.

## Running Tests

To run the unit tests, use:Pytest



## Interactive API Documentation

You can explore and test all API endpoints using the FastAPI interactive docs:

- [OpenAPI/Swagger UI](http://127.0.0.1:8000/docs)