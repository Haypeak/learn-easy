# Learn-Easy Learning Platform

A full-stack learning platform built with Flask (backend) and React (frontend) that provides an interactive environment for online education.

## Project Overview

Learn-Easy is a comprehensive learning management system designed to facilitate online education through:
- Course creation and management
- Student enrollment and progress tracking
- Interactive learning materials
- Assessment and feedback mechanisms

## Prerequisites

Before you begin, ensure you have the following installed:

### Backend Requirements
- Python 3.x
- pip (Python package manager)
- MongoDB Atlas account

### Frontend Requirements
- Node.js (v14.x or later)
- npm (v6.x or later)

## Installation

### Setting Up the Backend (Flask)

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd learn-easy
   ```

2. **Create and activate a virtual environment**:
   ```
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install backend dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Create a .env file** in the root directory with the following variables:
   ```
   MONGO_URI=your_mongodb_atlas_connection_string
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

### Setting Up the Frontend (React)

1. **Navigate to the frontend directory**:
   ```
   cd frontend
   ```

2. **Create a .env file** in the frontend directory:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

3. **Install frontend dependencies**:
   ```
   npm install
   ```

## Running the Application

### Development Mode

1. **Start the backend server** (from the root directory):
   ```
   # Make sure virtual environment is activated
   flask run
   ```
   The backend server will start at `http://localhost:5000`.

2. **Start the frontend development server** (in a separate terminal, from the frontend directory):
   ```
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

### Production Mode

1. **Build the frontend**:
   ```
   cd frontend
   npm run build
   ```

2. **Set environment variable**:
   ```
   # Windows
   set FLASK_ENV=production
   
   # macOS/Linux
   export FLASK_ENV=production
   ```

3. **Run the application**:
   ```
   gunicorn -w 4 run:app
   ```

## Environment Variables Guide

### Backend Environment Variables (.env in root directory)

| Variable | Description | Example |
|----------|-------------|---------|
| MONGO_URI | MongoDB Atlas connection string | mongodb+srv://username:password@cluster.mongodb.net/database |
| SECRET_KEY | Flask secret key for session security | your_random_string_here |
| JWT_SECRET_KEY | Secret key for JWT token generation | another_random_string_here |
| FLASK_APP | Entry point for the Flask application | run.py |
| FLASK_ENV | Application environment (development/production) | development |

### Frontend Environment Variables (.env in frontend directory)

| Variable | Description | Example |
|----------|-------------|---------|
| REACT_APP_API_URL | Backend API URL | http://localhost:5000 |

## Project Structure

```
learn-easy/
├── app/                   # Flask application
│   ├── __init__.py        # Application factory
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   └── services/          # Business logic
├── config.py              # Configuration settings
├── frontend/              # React frontend
│   ├── public/            # Static files
│   ├── src/               # Source code
│   └── package.json       # npm dependencies
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Troubleshooting

- **MongoDB Connection Issues**: Ensure your MongoDB Atlas IP whitelist includes your current IP address.
- **CORS Errors**: Check that the frontend URL is correctly included in the CORS_ORIGINS setting.
- **Missing Dependencies**: Run `pip install -r requirements.txt` and `npm install` to ensure all dependencies are installed.

# learn-easy