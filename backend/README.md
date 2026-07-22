# Backend

Backend service for the **Student Early Warning System**.

The backend is built with **Laravel** and serves as the central coordinator between the Vue frontend and the FastAPI-based AI prediction service. It handles request validation, data preprocessing, prediction workflows, file processing, and prediction history management.

---

# Architecture

```text
Vue Frontend
      │
      ▼
Laravel Backend
      │
      ▼
FastAPI AI Server
      │
      ▼
Machine Learning Model
```

The Laravel backend is responsible for orchestrating the entire prediction workflow while remaining independent of the machine learning implementation.

---

# Responsibilities

- RESTful API development
- Student data validation
- Single prediction processing
- Batch prediction processing
- Excel file upload and parsing
- Communication with AI Server
- Prediction history management
- JSON-based local storage
- Response formatting
- Error handling

---

# Core Features

## Single Prediction

Predict the academic risk level of an individual student.

Workflow:

```text
Frontend
    │
    ▼
Validate Input
    │
    ▼
Call AI Server
    │
    ▼
Receive Prediction
    │
    ▼
Save History
    │
    ▼
Return Result
```

---

## Batch Prediction

Predict multiple students simultaneously using Excel files.

Features:

- Upload Excel (.xlsx)
- Parse student records
- Validate each record
- Send batch requests to AI Server
- Generate prediction results
- Export prediction report

---

## Prediction History

Store prediction sessions locally.

Current implementation:

- JSON storage
- Timestamp
- Prediction result
- Risk level
- Recommendation
- Uploaded filename (batch mode)

---

# Project Structure

```text
backend/
│
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   ├── Middleware/
│   │   └── Requests/
│   │
│   ├── Models/
│   └── Services/
│       ├── AIService.php
│       ├── ExcelService.php
│       └── HistoryService.php
│
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
│   ├── api.php
│   ├── web.php
│   └── console.php
│
├── storage/
│   ├── uploads/
│   └── predictions/
│
├── tests/
│
├── composer.json
└── README.md
```

---

# API Modules

## Prediction API

- Single Prediction
- Batch Prediction

---

## History API

- Get prediction history
- Delete history
- Search history

---

## File API

- Upload Excel
- Download prediction results
- Download template

---

## System API

- Health Check
- AI Server Status

---

# Workflow

```text
User
 │
 ▼
Vue Frontend
 │
 ▼
Laravel API
 │
 ├──────────────┐
 │              │
 ▼              ▼
Validation   Excel Parser
 │              │
 └──────┬───────┘
        ▼
 Data Processing
        │
        ▼
 FastAPI AI Server
        │
        ▼
 Prediction Result
        │
        ▼
 Save JSON History
        │
        ▼
 API Response
```

---

# Technologies

| Layer | Technology |
|--------|------------|
| Framework | Laravel 13 |
| Language | PHP 8.3 |
| API | RESTful API |
| File Processing | Laravel Excel |
| HTTP Client | Laravel HTTP Client |
| Storage | JSON |
| AI Communication | FastAPI |
| Data Format | JSON |

---

# Development Roadmap

## Phase 1

- REST API
- Single Prediction
- Batch Prediction
- Excel Upload
- JSON History

---

## Phase 2

- SQLite/MySQL Integration
- Authentication
- User Management
- Role-based Authorization

---

## Phase 3

- Dashboard Analytics
- Prediction Statistics
- Notification System
- Logging & Monitoring
- API Documentation (Swagger/OpenAPI)

---

# Development Status

| Module | Status |
|---------|--------|
| Laravel Setup | ✅ |
| REST API | 🚧 |
| Single Prediction | ⏳ |
| Batch Prediction | ⏳ |
| Excel Processing | ⏳ |
| AI Communication | ⏳ |
| History Storage | ⏳ |
| Authentication | 📅 Planned |
| Database | 📅 Planned |

---

# Notes

This backend is intentionally designed to remain independent of the machine learning implementation. The AI model can be updated or replaced without affecting the frontend or backend architecture, as long as the FastAPI service maintains a consistent API contract.