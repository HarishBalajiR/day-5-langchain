# Day 5 - LangChain Student Marks Agent

A LangChain ReAct agent that answers student-related queries by autonomously selecting and chaining the right tools. Built with LangGraph and Groq.

## Architecture

```
User Question
      |
     LLM (Groq - Qwen 27B)
      |
Which tool is needed?
      |
   Tool(s) execute
      |
     LLM
      |
Need another tool? -- yes --> loop back
      |
   no
      |
Final Answer
```

## Tools

| Tool | Type | Purpose |
|------|------|---------|
| `get_student_info` | Read-only | Fetch name and department from SQLite |
| `get_student_marks` | Read-only | Fetch marks in all four subjects |
| `calculator` | Compute | Evaluate arithmetic expressions (totals, averages) |
| `get_passing_rules` | Read-only | Return university passing criteria |

## Database

A SQLite database (`students.db`) is seeded automatically at runtime with 5 students:

| student_id | name | department | python | database | ai | web |
|---|---|---|---|---|---|---|
| 22CS045 | Dhanushya | Computer Science | 85 | 72 | 90 | 78 |
| 22CS046 | Rahul | Computer Science | 65 | 70 | 68 | 72 |
| 22CS047 | Priya | Information Technology | 92 | 88 | 95 | 90 |
| 22CS048 | Arun | Information Technology | 55 | 60 | 58 | 62 |
| 22CS049 | Meena | Computer Science | 78 | 85 | 80 | 88 |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# paste your Groq API key in .env
```

## Run

```bash
python main.py
```

## Sample Queries

The agent handles these autonomously, deciding which tools to call and in what order:

1. **Single tool** - "What is the name and department of student 22CS045?"
2. **Single tool** - "What are the marks of 22CS047?"
3. **Two tools chained** - "What is the total and average mark of 22CS045?"
4. **Three tools chained** - "Is 22CS045 eligible to pass according to the university rules?"
5. **All four tools** - "I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements."

## Tech Stack

- **LangChain** + **LangGraph** (ReAct agent with tool calling)
- **Groq** (Qwen 27B via `langchain-groq`)
- **SQLite** (student data)
- **python-dotenv** (env config)
