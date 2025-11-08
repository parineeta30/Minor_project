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

