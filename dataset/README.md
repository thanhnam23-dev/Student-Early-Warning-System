# Dataset

This directory contains datasets, preprocessing resources, and Excel templates used by the Student Early Warning System.

---

## Purpose

The datasets are used for:

- Machine Learning model training
- Model evaluation
- Batch prediction
- System demonstration

---

## Suggested Structure

```text
dataset/
│
├── raw/
│
├── processed/
│
├── template/
│   └── student_template.xlsx
│
├── sample/
│
└── README.md
```

---

## Directories

### raw/

Original datasets collected from public sources.

Example:

- student_dropout.csv

---

### processed/

Processed datasets after cleaning, encoding, and feature engineering.

---

### template/

Excel templates for Batch Prediction.

Users should download the template, fill in student information, and upload it to the system.

---

### sample/

Sample files for testing the system.

---

## Dataset Information

Main dataset:

Predict Students' Dropout and Academic Success

Target labels:

- Graduate
- Dropout
- Enrolled

---

## Notes

- Do not modify the original dataset.
- Store cleaned datasets inside the **processed/** directory.
- Keep template files synchronized with the backend import format.