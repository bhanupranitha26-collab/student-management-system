# Student Management System (Python + CSV)

A simple console-based Student Management System built with Python.
Data is stored in a CSV file (`students.csv`). The system supports:
- Add student (auto-increment id, unique roll)
- View all students
- Search by roll number
- Update student details
- Delete student

## Tech
- Python 3
- CSV file for persistence

## How to run
1. Clone or download the repository.
2. (Optional) Install tabulate for prettier tables:
   `pip install tabulate`
3. Run the app:
   `python student_mgmt.py`

## File structure
- `student_mgmt.py` - main program
- `students.csv` - data (created automatically if missing)

## Notes
- Roll numbers are unique (case-insensitive).
- ID is auto-generated.
