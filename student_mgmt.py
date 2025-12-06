#!/usr/bin/env python3
"""
Student Management System (CSV-based)
Features:
- Add student (auto-increment id, unique roll)
- View all students
- Search by roll
- Update student
- Delete student
"""

import csv
import os
from tabulate import tabulate   # optional nice table display; fallback provided if not installed

DATA_FILE = "students.csv"
FIELDNAMES = ["id", "roll", "name", "branch", "year", "email", "phone"]


def ensure_datafile():
    """Ensure CSV exists with headers."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all_students():
    ensure_datafile()
    with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_all_students(students):
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for s in students:
            writer.writerow(s)


def next_id(students):
    if not students:
        return "1"
    ids = [int(s["id"]) for s in students if s["id"].isdigit()]
    return str(max(ids) + 1)


def find_by_roll(students, roll):
    for s in students:
        if s["roll"].lower() == roll.lower():
            return s
    return None


def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.")


def add_student():
    students = read_all_students()
    roll = input_nonempty("Enter roll number: ")
    if find_by_roll(students, roll):
        print(f"Error: Student with roll '{roll}' already exists.")
        return
    name = input_nonempty("Enter name: ")
    branch = input_nonempty("Enter branch: ")
    year = input_nonempty("Enter year (ex: 1/2/3/4): ")
    email = input("Enter email (optional): ").strip()
    phone = input("Enter phone (optional): ").strip()
    sid = next_id(students)
    student = {
        "id": sid,
        "roll": roll,
        "name": name,
        "branch": branch,
        "year": year,
        "email": email,
        "phone": phone,
    }
    students.append(student)
    write_all_students(students)
    print("Student added successfully.")


def view_students():
    students = read_all_students()
    if not students:
        print("No students found.")
        return
    # Pretty table if tabulate installed
    try:
        table = [[s[f] for f in FIELDNAMES] for s in students]
        print(tabulate(table, headers=FIELDNAMES, tablefmt="grid"))
    except Exception:
        # Fallback simple print
        for s in students:
            print(", ".join(f"{k}: {s[k]}" for k in FIELDNAMES))
            print("-" * 40)


def search_student():
    roll = input_nonempty("Enter roll number to search: ")
    students = read_all_students()
    s = find_by_roll(students, roll)
    if not s:
        print("Student not found.")
        return
    print("Student found:")
    for k in FIELDNAMES:
        print(f"{k}: {s[k]}")


def update_student():
    roll = input_nonempty("Enter roll number to update: ")
    students = read_all_students()
    s = find_by_roll(students, roll)
    if not s:
        print("Student not found.")
        return
    print("Leave blank to keep existing value.")
    new_name = input(f"Name [{s['name']}]: ").strip() or s["name"]
    new_branch = input(f"Branch [{s['branch']}]: ").strip() or s["branch"]
    new_year = input(f"Year [{s['year']}]: ").strip() or s["year"]
    new_email = input(f"Email [{s['email']}]: ").strip() or s["email"]
    new_phone = input(f"Phone [{s['phone']}]: ").strip() or s["phone"]

    # Update entry
    for student in students:
        if student["roll"].lower() == roll.lower():
            student.update({
                "name": new_name,
                "branch": new_branch,
                "year": new_year,
                "email": new_email,
                "phone": new_phone,
            })
            break
    write_all_students(students)
    print("Student updated successfully.")


def delete_student():
    roll = input_nonempty("Enter roll number to delete: ")
    students = read_all_students()
    s = find_by_roll(students, roll)
    if not s:
        print("Student not found.")
        return
    confirm = input(f"Are you sure you want to delete {s['name']} (y/N)? ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return
    students = [st for st in students if st["roll"].lower() != roll.lower()]
    write_all_students(students)
    print("Student deleted successfully.")


def menu():
    options = {
        "1": ("Add student", add_student),
        "2": ("View all students", view_students),
        "3": ("Search by roll", search_student),
        "4": ("Update student", update_student),
        "5": ("Delete student", delete_student),
        "6": ("Exit", None),
    }
    while True:
        print("\n----- Student Management -----")
        for k, v in options.items():
            print(f"{k}. {v[0]}")
        choice = input("Choose an option: ").strip()
        if choice not in options:
            print("Invalid choice. Try again.")
            continue
        if choice == "6":
            print("Goodbye!")
            break
        try:
            options[choice][1]()
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting... bye!")
