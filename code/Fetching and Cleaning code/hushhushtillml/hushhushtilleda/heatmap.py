import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

INPUT_CSV_FILE = 'FEATURE_ENGINEERED12.csv'


try:
    df = pd.read_csv(INPUT_CSV_FILE)
    print(f" Successfully loaded '{INPUT_CSV_FILE}' to generate heatmap.\n")
except FileNotFoundError:
    print(f" Error: The file '{INPUT_CSV_FILE}' was not found.")
    exit()

# We can only calculate correlation for numerical columns.
numerical_df = df.select_dtypes(include=['number'])

print("--- Analyzing correlations for the following features: ---")
for col in numerical_df.columns:
    print(f"- {col}")

# --- 3. CALCULATE THE CORRELATION MATRIX ---

corr_matrix = numerical_df.corr()

# --- 4. GENERATE AND DISPLAY THE HEATMAP ---
print("\n Generating Correlation Heatmap ")

# Set the size of the plot to make it readable
plt.figure(figsize=(14, 10))

# Use seaborn to create the heatmap
# annot=True displays the numbers on the map
# annot_kws reduces the font size of the numbers to prevent overlap
# cmap='coolwarm' is a good color scheme (red for positive, blue for negative)
# fmt='.2f' formats the numbers to two decimal places
sns.heatmap(
    corr_matrix, 
    annot=True, 
    fmt='.2f', 
    cmap='coolwarm', 
    linewidths=.5,
    annot_kws={"size": 8} # Reduced font size for annotations
)

# Add a title to the plot
plt.title('Correlation Matrix of All Features', fontsize=18)

# Rotate the x-axis labels to prevent them from overlapping
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Adjust layout to make sure everything fits without being cut off
plt.tight_layout()

# Display the plot
plt.show()

print("\nHeatmap generation complete.")

