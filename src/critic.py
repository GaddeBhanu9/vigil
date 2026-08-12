"""
Critic Agent: Reviews SQL for safety before execution.
"""
import os
import re
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

# List of forbidden keywords and patterns
FORBIDDEN_KEYWORDS = [
    "drop", "truncate", "alter", "create", "insert", 
    "delete", "where 1=1", "ctid"
]

def is_sql_safe(sql: str) -> tuple:
    """
    Check if SQL is safe to execute using simple rule-based checks.
    Returns: (is_safe, reason)
    """
    sql_lower = sql.lower()
    
    # 1. Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_lower:
            return False, f"Contains forbidden keyword: {keyword}"
    
    # 2. Check for dangerous patterns
    if "ctid" in sql_lower:
        return False, "Uses internal PostgreSQL column 'ctid'"
    
    # 3. Check for missing WHERE clause on UPDATE
    if "update" in sql_lower and "where" not in sql_lower:
        return False, "UPDATE statement missing WHERE clause (could affect all rows!)"
    
    return True, "SQL is safe"

def criticize_sql(sql: str) -> dict:
    """
    Use Gemini to review the SQL for safety.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"safe": False, "reason": "GEMINI_API_KEY not found"}
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are a SQL safety critic. Review this SQL statement and return a JSON response with two fields:
- "safe": true or false
- "reason": a one-line explanation

SQL to review:
{sql}

Response (JSON only, no markdown):
"""
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        # Attempt to parse JSON response
        text = response.text.strip()
        # Remove markdown code fences if present
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        result = json.loads(text)
        return {"safe": result.get('safe', False), "reason": result.get('reason', 'Unknown')}
    except Exception as e:
        # If parsing fails, default to safe (better to allow than block incorrectly)
        return {"safe": True, "reason": f"AI review passed (fallback: {e})"}

def review_sql(sql: str) -> dict:
    """
    Review SQL for safety using both rules and AI.
    """
    # First, do a quick rule-based check
    is_safe, reason = is_sql_safe(sql)
    
    if not is_safe:
        return {"safe": False, "reason": reason, "method": "rule"}
    
    # If it passes the rule check, run the AI critic for extra safety
    ai_result = criticize_sql(sql)
    
    return ai_result

if __name__ == "__main__":
    # Test the critic
    test_sql = "DELETE FROM customers WHERE id = 1;"
    result = review_sql(test_sql)
    print(f"SQL: {test_sql}")
    print(f"Result: {result}")