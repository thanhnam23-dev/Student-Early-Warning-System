# Backend

Backend service for the Student Early Warning System.

## Overview

The backend acts as the central coordinator between the frontend and the AI prediction service. It is responsible for processing user requests, validating input data, managing prediction history, and communicating with the AI server.

---

## Responsibilities

- RESTful API
- Single prediction request
- Batch prediction request
- Excel file processing
- Input validation
- Prediction history management
- JSON storage
- Communication with AI Server

---

## Main Features

### Single Prediction

Receive a student's information from the frontend and forward the processed data to the AI server.

### Batch Prediction

- Upload Excel files
- Parse student records
- Send prediction requests
- Return prediction results
- Export processed results

### Prediction History

Store prediction sessions as JSON files for future reference.

---

## Project Structure

```text
backend/
│
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
├── storage/
│   ├── uploads/
│   └── predictions/
├── tests/
│
└── README.md
```

---

## Workflow

```text
Frontend
    │
    ▼
Validate Request
    │
    ▼
Process Input
    │
    ▼
Call AI Server
    │
    ▼
Receive Prediction
    │
    ▼
Save JSON
    │
    ▼
Return Response
```

---

## Technologies

- Laravel
- PHP
- REST API
- JSON Storage

---

## Future Improvements

- Database integration
- Authentication
- Role-based authorization
- Prediction analytics
- Notification system