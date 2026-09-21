import os
import sys
import sqlite3
import warnings

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

DB = "students.db"


def seed_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY, name TEXT, department TEXT,
        python INTEGER, database INTEGER, ai INTEGER, web INTEGER)""")
    conn.executemany(
        "INSERT OR IGNORE INTO students VALUES (?,?,?,?,?,?,?)",
        [("22CS045", "Dhanushya", "Computer Science", 85, 72, 90, 78),
         ("22CS046", "Rahul", "Computer Science", 65, 70, 68, 72),
         ("22CS047", "Priya", "Information Technology", 92, 88, 95, 90),
         ("22CS048", "Arun", "Information Technology", 55, 60, 58, 62),
         ("22CS049", "Meena", "Computer Science", 78, 85, 80, 88)])
    conn.commit()
    conn.close()


def query(sql, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


@tool
def get_student_info(student_id: str) -> dict:
    """Look up a student's name and department by their roll number."""
    rows = query("SELECT name, department FROM students WHERE student_id = ?", (student_id,))
    return rows[0] if rows else {"error": f"No student with id {student_id}"}


@tool
def get_student_marks(student_id: str) -> dict:
    """Look up a student's marks in all four subjects: python, database, ai, web."""
    rows = query("SELECT python, database, ai, web FROM students WHERE student_id = ?", (student_id,))
    return rows[0] if rows else {"error": f"No student with id {student_id}"}


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result. Example: '85+72+90+78'."""
    return str(eval(expression))


@tool
def get_passing_rules() -> dict:
    """Return the university passing rules: minimum overall average and minimum per-subject mark."""
    return {"min_average": 40, "min_per_subject": 35}


QUESTIONS = [
    "What is the name and department of student 22CS045?",
    "What are the marks of 22CS047?",
    "What is the total and average mark of 22CS045?",
    "Is 22CS045 eligible to pass according to the university rules?",
    "I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements.",
]


def main():
    seed_db()

    llm = ChatGroq(model="qwen/qwen3.8-27b")
    agent = create_react_agent(llm, [get_student_info, get_student_marks, calculator, get_passing_rules])

    for q in QUESTIONS:
        print(f"\n{'='*70}\nQ: {q}\n{'='*70}")
        result = agent.invoke({"messages": [("user", q)]})
        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
