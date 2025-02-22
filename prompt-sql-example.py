from transformers import pipeline
from langchain_community.utilities.sql_database import SQLDatabase

model_name = "defog/sqlcoder"  # SQL-specific LLM
sql_pipeline = pipeline("text-generation", model=model_name, device="cpu")


# Function to generate SQL query
def generate_sql(prompt):
    """Generate an SQL query from a natural language prompt."""
    input_prompt = f"Convert this to an SQL query: {prompt}"
    
    result = sql_pipeline(input_prompt, max_length=200, do_sample=True)
    generated_sql = result[0]['generated_text']
    
    return generated_sql


# Example Usage
user_prompt = "Find all movies released after 2010 with a rating above 8."

print(generate_sql(user_prompt))