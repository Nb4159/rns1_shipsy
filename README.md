# Task Management Application

## Project Overview

This is a full-stack task management application with a React frontend and a Flask backend.

## Features

- User registration and login with JWT authentication.
- Create, read, update, and delete tasks.
- Filter tasks by overdue status, urgency (priority), and complexity.

## API Documentation

### Authentication

- **POST /register**
  - Creates a new user.
  - Request body: `{"username": "your-username", "password": "your-password"}`
  - Response: `{"message": "User created successfully"}`

- **POST /login**
  - Logs in a user and returns a JWT token.
  - Request body: `{"username": "your-username", "password": "your-password"}`
  - Response: `{"token": "your-jwt-token"}`

### Tasks

- **GET /tasks**
  - Returns a paginated list of tasks for the authenticated user.
  - Query parameters:
    - `page`: The page number to retrieve.
    - `overdue`: `true` to filter for overdue tasks.
    - `urgency`: `Low`, `Medium`, or `High` to filter by urgency.
    - `complexity`: `Low`, `Medium`, or `High` to filter by complexity.

- **POST /tasks**
  - Creates a new task.
  - Request body: `{"title": "Task title", "description": "Task description", "priority": "Medium", "complexity": "Medium", "due_date": "YYYY-MM-DD"}`

- **GET /tasks/<task_id>**
  - Returns a single task.

- **PUT /tasks/<task_id>**
  - Updates a task.

- **DELETE /tasks/<task_id>**
  - Deletes a task.

## Getting Started

### Prerequisites

- Python 3.11
- Node.js and npm

### Installation

1.  **Backend:**
    ```bash
    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Frontend:**
    ```bash
    cd frontend
    npm install
    ```

### Running the application

1.  **Backend:**
    ```bash
    cd backend
    venv\Scripts\activate
    python app.py
    ```

2.  **Frontend:**
    ```bash
    cd frontend
    npm start
    ```

## Deployment

### Vercel (for the frontend)

1.  Sign up for a Vercel account.
2.  Connect your GitHub account and select the repository for this project.
3.  Configure the project:
    -   **Framework Preset:** Create React App
    -   **Build Command:** `npm run build`
    -   **Output Directory:** `build`
    -   **Install Command:** `npm install`
4.  Add an environment variable for the backend URL:
    -   `REACT_APP_API_URL`: The URL of your deployed backend (e.g., from Render).
5.  Deploy the project.

### Render (for the backend)

1.  Sign up for a Render account.
2.  Create a new "Web Service".
3.  Connect your GitHub account and select the repository for this project.
4.  Configure the service:
    -   **Name:** A name for your service.
    -   **Region:** Choose a region.
    -   **Branch:** `master`
    -   **Root Directory:** `backend`
    -   **Build Command:** `pip install -r requirements.txt`
    -   **Start Command:** `gunicorn app:app`
5.  Deploy the service.
