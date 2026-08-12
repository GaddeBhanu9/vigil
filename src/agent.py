"""
Auto-Healing Agent for Project VIGIL using Google Gemini.
Reads data quality issues and generates corrective SQL.
"""
import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

def clean_sql_output(text: str) -> str:
    """
    Remove markdown code fences and extra whitespace from generated SQL.
    """
    text = re.sub(r'```sql\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    return text.strip()

def get_sql_fix(issue_description: str, table_name: str = "customers") -> str:
    """
    Generate a corrective SQL statement for a given data quality issue.
    """
    prompt = f"""
You are an expert PostgreSQL engineer. Your task is to generate a single, safe SQL UPDATE statement to fix a data quality issue in a table named '{table_name}'.

The columns in this table are: CustomerID, Name, Gender, Age, City, Signup_Date, Last_purchase_date, purchase_amount, feedback_score, email, Phone_number, Country.

Rules for generating the fix:
- Only output the SQL statement itself. Do not wrap it in markdown backticks, do not include explanations.
- Use double quotes for column names if they are case-sensitive.
- For NULL values: set the column to a safe default:
    - email → 'unknown@example.com'
    - Phone_number → '0000000000'
    - Age → NULL (if you can't infer a safe default)
    - purchase_amount → 0
    - feedback_score → 5
- For negative values in numeric columns (Age, purchase_amount, feedback_score): set them to 0 or NULL.
- For duplicate CustomerID: write a query that deletes duplicates, keeping the row with the smallest CustomerID. 
  If it's not safe to delete, output '-- Manual review required'.
- For invalid email format (missing '@'): set email to NULL.
- Ensure the WHERE clause targets only the problematic rows.
- If absolutely no safe fix is possible, output '-- No safe fix available'.

Now, generate the fix for this issue:
Issue: {issue_description}

SQL UPDATE statement:
"""
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        sql = response.text.strip()
        sql = clean_sql_output(sql)
        return sql
    except Exception as e:
        return f"-- Error generating SQL fix: {e}"

if __name__ == "__main__":
    # Test with an example issue
    test_issue = "Email column has NULL values"
    print("=" * 60)
    print("🤖 TESTING AUTO-HEALING AGENT")
    print("=" * 60)
    print(f"📋 Issue: {test_issue}\n")
    
    sql = get_sql_fix(test_issue)
    print("📝 Generated SQL Fix:")
    print("-" * 40)
    print(sql)
    print("-" * 40)