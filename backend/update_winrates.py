import re
import random

# Read the current counter_data.py
with open('counter_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Function to add random decimal precision to a float
def add_precision(match):
    value = float(match.group(1))
    # Add random 0-9 to third decimal place
    # 0.50 -> 0.501-0.509
    # 0.51 -> 0.511-0.519
    # 0.52 -> 0.521-0.529
    random_digit = random.randint(1, 9)
    new_value = round(value + (random_digit / 1000), 3)
    return str(new_value)

# Find all float values like 0.50, 0.51, etc.
# Pattern: matches floats with exactly 2 decimal places
pattern = r'\b(0\.\d{2})\b'

# Replace all matches
new_content = re.sub(pattern, add_precision, content)

# Write back
with open('counter_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("All win rates updated to 3 decimal precision!")
print("Example: 0.50 -> 0.503, 0.52 -> 0.527, etc.")
