# Smart Task Analyzer

A mini application that analyzes and prioritizes tasks using a custom scoring algorithm.

## Features
- Form-based task input
- Intelligent scoring algorithm
- Django backend API
- Clean frontend UI
- Unit tests for scoring logic

## Scoring Logic
- Overdue tasks → +100
- Due in ≤3 days → +50
- Importance × 5
- Quick tasks (<2 hrs) → +10

## How to Run
1. python -m venv venv
2. Activate environment
3. pip install django django-cors-headers
4. python manage.py migrate
5. python manage.py runserver 0.0.0.0:8000
6. Open frontend/index.html using Live Server

## Tests
Run:
```
python manage.py test tasks
```

## Project Structure
task-analyzer/
├── backend/
├── tasks/
├── frontend/
└── README.md
