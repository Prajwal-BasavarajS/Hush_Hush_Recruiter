import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns


INPUT_CSV_FILE = 'FEATURE_ENGINEERED12.csv'
OUTPUT_CSV_FILE = 'NORMALIZED_FEATURES.csv'


try:
    df = pd.read_csv(INPUT_CSV_FILE)
    print(f" Successfully loaded '{INPUT_CSV_FILE}' for Normalization.\n")
except FileNotFoundError:
    print(f" Error: The file '{INPUT_CSV_FILE}' was not found.")
    exit()

#  SEPARATE IDENTIFIERS FROM NUMERICAL FEATURES ---
identifier_cols = ['owner', 'email']
existing_identifier_cols = [col for col in identifier_cols if col in df.columns]
numerical_cols = df.select_dtypes(include=['number']).columns
df_numerical = df[numerical_cols]

print("--- Applying Normalization (0-to-1 scaling) to the following features: ---")
for col in numerical_cols:
    print(f"- {col}")

#  APPLY NORMALIZATION (MIN-MAX SCALING) ---
# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Fit the scaler to the data and transform it
# This rescales the data to a range between 0 and 1
normalized_features = scaler.fit_transform(df_numerical)

# Create a new DataFrame with the normalized data and the original column names
df_normalized = pd.DataFrame(normalized_features, columns=numerical_cols)


# --- 4. COMBINE AND SAVE THE FINAL DATASET ---
if existing_identifier_cols:
    df_final = pd.concat([df[existing_identifier_cols].reset_index(drop=True), df_normalized], axis=1)
else:
    df_final = df_normalized

print("\n--- Preview of Data Before Normalization ---")
print(df.head())

print("\n--- Preview of Data After Normalization (Scaled to 0-1) ---")
print(df_final.head())


# Save the final, model-ready dataframe to a new CSV file
df_final.to_csv(OUTPUT_CSV_FILE, index=False)
print(f"\n Normalization complete. The model-ready data has been saved to '{OUTPUT_CSV_FILE}'.")

