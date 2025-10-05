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

### Usage

Once the application is deployed, you can access the frontend at the URL provided by your hosting service (e.g., Vercel). The frontend will make requests to the backend API.

## Deployment

The frontend of this application is designed to be deployed on a service like Vercel. The backend is a separate Flask application that needs to be deployed as a web service on a platform that supports Python, such as Render or Heroku.

When deploying the frontend, you will need to set the `REACT_APP_API_URL` environment variable to the URL of your deployed backend.
