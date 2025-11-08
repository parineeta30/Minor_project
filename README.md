# Conflict News Bias Detector
## Overview:
Conflict News Bias Detector is a web application designed to analyze news articles for bias in coverage of conflict-related topics. It consists of a frontend for user interaction and a backend for processing and analysis.

**## Features Upload or paste news articles for bias analysis

Visualize analysis results in a user-friendly format

Supports articles on conflict topics

Designed for educational and research purposes

## Project Structure
news-bias-detector/
│
├── backend/
│   ├── app.py
│   ├── ... (other backend code, e.g. models, routes, utils,.env files etc.)
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │    ├── App.js
│   │    ├── index.js
│   │    └── ... (other React components, files)
│   ├── public/
│   │    └── index.html
│   ├── package.json
│   ├── package-lock.json (or yarn.lock)
│   └── .gitignore
│
├── requirements.txt
├── README.md
├── env folder(on your local machine acc. to requirements.txt)
└── .gitignore


## Setup Instructions### Prereisites

Python 3.x installed

Node.js and npm (if frontend uses JavaScript frameworks)

Git

### Backendetup 
# Clone the repository
git clone https://github.com/yourusername/conflict-news-bias-detector.git
cd conflict-news-bias-detector/backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py  # or your main backend file

### Frontend Setup
cd ../frontend

# Install frontend dependencies
npm install

# Run the frontend server
npm start

### What I Have Built So Far + TECH STACK (yet)
1. Backend (Flask + Python + ML)
Built a Flask backend in Python.

Fetches the latest news articles from global sources using RSS feeds.

Uses a pre-trained BERT (transformer) model to analyze sentiment of each article.

Applies basic rules to estimate bias (left, right, neutral).

Exposes REST API endpoints for news, stats, and analysis.

2. Frontend (React Dashboard)
Built a React.js dashboard (with charts and tables).

Displays live bias and sentiment stats for analyzed articles.

Shows a list of articles with their bias/sentiment labels and direct links.

“Fetch Latest News” button triggers backend analysis and data refresh.

3. Machine Learning Integration
BERT model is used in backend to automatically analyze news text for sentiment and bias.

Analysis is automated—each time new articles are fetched, the ML model generates results.

4. Project Flow
Backend server runs API and ML analysis.

Frontend dashboard connects to backend, fetches data, and shows it visually.

5. Learning Process
Followed a structured approach, setting up project folders, installing required packages, and wiring up backend APIs to frontend.

Used online resources and step-by-step help for troubleshooting and implementation.

Successfully fixed errors, managed dependencies, and visualized results from ML predictions.

In short:
I’ve created a working news bias detection app with a Python/Flask backend (using BERT ML model), and a React dashboard frontend. Right now it analyzes and displays bias/sentiment of global news articles, fully working end-to-end.

## How to start :

1. Start Backend (Flask) API
In your project root or backend folder:

Open a new Command Prompt.

Activate your Python environment: cd C:\Users\...\news-bias-detector
.\news_bias_env\Scripts\activate

** Move to backend folder:

cd backend

** Start Flask backend:

python app.py

** Leave this terminal running! **

2. Start Frontend (React App)
In a second new Command Prompt:
Go to your frontend folder:

cd C:\Users\...\news-bias-detector\frontend
Start React frontend:

npm start
(Your browser will open at localhost:3000)


