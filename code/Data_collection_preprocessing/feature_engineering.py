import pandas as pd
import numpy as np

INPUT_CSV_FILE = 'CLEANEDD.csv'
OUTPUT_CSV_FILE = 'FEATURE_ENGINEERED12.csv'
try:
    df = pd.read_csv(INPUT_CSV_FILE)
    print(f" Successfully loaded '{INPUT_CSV_FILE}' for Feature Engineering.\n")
except FileNotFoundError:
    print(f" Error: The file '{INPUT_CSV_FILE}' was not found.")
    exit()

#  FEATURE ENGINEERING: CREATE ONLY TWO FEATURES 
print("---  Engineering New Features ---")

epsilon = 1e-6  # To avoid division by zero

# Feature 1: issue_closure_rate (Responsibility Score)
df['issue_closure_rate'] = df['owner_issues_closed'] / (df['owner_issues_opened'] + epsilon)
df['issue_closure_rate'] = np.clip(df['issue_closure_rate'], 0, 1) * 100  # percentage
df['issue_closure_rate'] = df['issue_closure_rate'].round().astype(int)
print("  - Created 'issue_closure_rate' (as whole number percentage)")

# Feature 2: forks_to_stars_ratio (Developer’s Developer Score)
df['forks_to_stars_ratio'] = (df['forks'] / (df['stars'] + epsilon)).round(2)
print("  - Created 'forks_to_stars_ratio' (rounded to 2 decimals)")

# --- 3. DISPLAY RESULTS AND SAVE ---
print("\n--- Preview of Data with New Features ")
display_columns = ['owner', 'stars', 'forks', 'issue_closure_rate', 'forks_to_stars_ratio']
print(df[display_columns].head())

# Save to CSV
df.to_csv(OUTPUT_CSV_FILE, index=False)
print(f"\n Feature engineering complete. The new data has been saved to '{OUTPUT_CSV_FILE}'.")
