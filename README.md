# 🎓 Student Early Warning System

An AI-powered Early Warning System for predicting students at risk of academic failure or dropout using Machine Learning.

This project aims to assist universities in identifying students with potential academic risks at an early stage, enabling timely interventions and support.

---

## 📌 Features

- 🔍 Single Student Prediction
  - Enter student information manually.
  - Predict academic outcome using trained AI models.

- 📄 Batch Prediction
  - Upload an Excel file containing multiple students.
  - Predict results for the entire dataset.
  - Export prediction results.

- 📊 Dashboard
  - Overview of prediction statistics.
  - Distribution of prediction results.

- 📜 Prediction History
  - Store prediction sessions as JSON.
  - View previous prediction results.

---

## 🏗️ Project Structure

```text
Student-Early-Warning-System/
│
├── ai-server/          # AI models & prediction API
├── backend/            # Backend REST API
├── frontend/           # Vue frontend
├── dataset/            # Dataset & Excel templates
├── docs/               # Documentation
│
├── README.md
└── .gitignore
```

---

## ⚙️ System Architecture

```text
                +----------------------+
                |      Frontend        |
                |       Vue 3          |
                +----------+-----------+
                           |
                      REST API
                           |
                +----------v-----------+
                |      Backend         |
                |   Business Logic     |
                +----------+-----------+
                           |
                HTTP Prediction API
                           |
                +----------v-----------+
                |      AI Server       |
                | Random Forest        |
                | XGBoost              |
                | LightGBM             |
                +----------+-----------+
                           |
                     Prediction Result
```

---

## 📁 Modules

### Frontend

Responsible for:

- Dashboard
- Single Prediction
- Batch Prediction
- Prediction History
- Result Visualization

---

### Backend

Responsible for:

- REST API
- File Upload
- Excel Processing
- Input Validation
- JSON Storage
- Communication with AI Server

---

### AI Server

Responsible for:

- Loading trained models
- Data preprocessing
- Model inference
- Returning prediction results

---

## 🚀 Workflow

```text
Single Prediction

Input Student Information
        │
        ▼
Backend Validation
        │
        ▼
AI Prediction
        │
        ▼
Prediction Result
        │
        ▼
Store JSON
```

---

```text
Batch Prediction

Upload Excel
      │
      ▼
Read Excel
      │
      ▼
Predict All Records
      │
      ▼
Generate Result
      │
      ▼
Export Excel
```

---

## 🤖 Machine Learning Models

The system is designed to support multiple machine learning models, including:

- Random Forest
- XGBoost
- LightGBM

The backend communicates with the AI server through REST APIs, allowing models to be replaced without modifying the frontend or backend logic.

---

## 📂 Dataset

Dataset used for training:

**Predict Students' Dropout and Academic Success**

Source:

- UCI Machine Learning Repository

Target Classes:

- Graduate
- Dropout
- Enrolled

---

## 🛠️ Technologies

### Frontend

- Vue 3
- TypeScript
- Vite
- Tailwind CSS
- PrimeVue
- Axios
- Vue Router
- Pinia

### Backend

- Laravel
- REST API
- PHP

### AI Server

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- Joblib

---

## 📈 Development Status

- [x] Project initialization
- [ ] AI model training
- [ ] AI prediction API
- [ ] Backend development
- [ ] Frontend development
- [ ] Excel import/export
- [ ] Prediction history
- [ ] System testing

---

## 👥 Team

Student Early Warning System

Research Project