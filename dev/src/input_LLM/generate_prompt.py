# generate_llm_prompt.py
# This script reads a CSV file of disasters (columns: name, status, link, time) and generates a prompt for an LLM
# to select the top 5 most relevant based on geographical closeness to a user location, importance, and recency.
# Usage: python generate_llm_prompt.py <csv_file> <location> [output_prompt.txt]

import sys
import csv
from datetime import datetime

def read_csv(csv_file: str) -> list[dict]:
    """Read CSV and return list of dicts with disaster data."""
    disasters = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse time if possible (assume format like 'YYYY-MM-DD' or similar)
            time_str = row.get('time', '')
            try:
                row['parsed_time'] = datetime.strptime(time_str, '%Y-%m-%d') if time_str else datetime.min
            except ValueError:
                row['parsed_time'] = datetime.min  # Fallback for invalid dates
            disasters.append(row)
    return disasters

def generate_prompt(disasters: list[dict], location: str) -> str:
    """Generate LLM prompt with CSV data and selection criteria."""
    # Format disasters as structured text
    formatted_data = "\n".join([
        f"- Name: {d['name']}\n  Status: {d['status']}\n  Link: {d['link']}\n  Time: {d['time']}\n  (Note: Location info may be in name/status; infer closeness to {location})"
        for d in disasters
    ])

    prompt = f"""
You are an expert disaster analyst. Given the following list of disasters from a CSV file, select the top 5 most relevant ones based on these criteria (prioritize in order):

1. **Geographical closeness** to our location: '{location}'. Infer location from name, status, or any context (e.g., country/city mentions). Rank closer ones higher.
2. **Importance of the issue**: Prioritize high-impact disasters (e.g., based on status like 'Ongoing' or 'Alert', scale of event implied in name).
3. **Recency bias**: Favor more recent events (use 'time' field; assume newer dates are more relevant).

Output only the top 5 in a numbered list, with brief reasoning for each selection. Include name, status, link, and time.

Disaster List:
{formatted_data}
"""
    return prompt

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_llm_prompt.py <csv_file> <location> [output_prompt.txt]")
        sys.exit(1)

    csv_file = sys.argv[1]
    location = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'prompt.txt'

    disasters = read_csv(csv_file)
    prompt_text = generate_prompt(disasters, location)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt_text)

    print(f"Generated prompt saved to {output_file}")
    print("\nPrompt Preview:\n" + prompt_text[:500] + "...")  # Truncated preview
