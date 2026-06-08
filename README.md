# MIRA - Health Prediction Application

A health prediction application built using **Python** and **Streamlit** that allows users to manage patient blood test records and generate AI-based health remarks using an external AI API.

## Project Overview

This application was developed as part of a technical assessment for a Junior AI/ML Developer role. The goal was to build a basic healthcare prediction system that can:

- store patient information,
- perform full CRUD operations,
- validate blood test and patient data,
- persist records using a local database,
- and generate AI-powered health remarks based on blood test values.

## Features

- Create, Read, Update, and Delete patient records
- Input validation for:
  - Full name
  - Email address
  - Date of birth
  - Numeric blood test values
- Persistent data storage using SQLite
- AI-generated health remarks using an external AI model
- Risk indicator based on entered lab values
- Clean and user-friendly Streamlit interface
- Reference ranges for blood test values shown in the UI

## Patient Data Fields

The application stores the following information for each patient:

- Full Name
- Date of Birth
- Email Address
- Glucose
- Haemoglobin
- Cholesterol
- Remarks (generated from AI)

## Tech Stack

| Layer | Technology |
|------|------------|
| Frontend / UI | Streamlit |
| Backend Logic | Python |
| Database | SQLite |
| AI Integration | Gemini API |
| Validation | Custom Python validation functions |

## Project Structure

```text
health-predictor/
├── .env.example
├── .gitignore
├── ai_service.py
├── app.py
├── database.py
├── requirements.txt
└── validators.py
```

## How It Works

1. The user enters patient details and blood test values.
2. The application validates the input fields.
3. Valid records are stored in the SQLite database.
4. The app sends blood test data to an external AI service.
5. The AI returns a short health-related remark.
6. The generated remark is stored and displayed in the application.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sashvatha20/MIRA.git
cd MIRA
```

### 2. Create and activate a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

## Validation Rules

The application includes basic validation such as:

- Email must be in a valid format
- Date of birth cannot be a future date
- Blood test values must be numeric
- Duplicate email handling during updates

## Notes

- The **Risk Indicator** shown in the UI is based on entered blood values and is used as a quick screening aid.
- The **AI-generated Remarks** are produced through external AI integration and are intended for demonstration purposes in this assessment.
- This project is not intended for real clinical diagnosis.

## Submission Notes

This project was created to demonstrate:

- problem-solving approach,
- code structure and maintainability,
- API integration,
- frontend and backend implementation,
- and GitHub project organization.

## Author

**Sashvatha**
