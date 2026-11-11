import pandas as pd

# 1. Load employee dataset
df = pd.read_csv("employees_cleaned.csv")

# Before cleaning summary
before_rows = len(df)
before_missing = int(df.isnull().sum().sum())
before_duplicates = int(df.duplicated().sum())

print("BEFORE CLEANING")
print("Rows:", before_rows)
print("Missing values:", before_missing)
print("Duplicates:", before_duplicates)

# 2. Remove rows with missing employee ID
df = df.dropna(subset=["employee_id"])

# 3. Fix data types
numeric_columns = [
    "age", "experience_years",
    "salary_inr", "performance_rating"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["joining_date"] = pd.to_datetime(
    df["joining_date"], errors="coerce"
)

# 4. Handle missing numeric values using median
for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

# Fill missing text values using mode
text_columns = ["name", "gender", "department", "city"]

for col in text_columns:
    mode_value = df[col].mode()
    if not mode_value.empty:
        df[col] = df[col].fillna(mode_value[0])

# Fill missing dates using median date
if df["joining_date"].isnull().any():
    median_date = df["joining_date"].dropna().median()
    df["joining_date"] = df["joining_date"].fillna(median_date)

# 5. Standardize text
df["employee_id"] = df["employee_id"].str.strip().str.upper()
df["name"] = df["name"].str.strip().str.title()
df["gender"] = df["gender"].str.strip().str.title()
df["department"] = df["department"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()

df["department"] = df["department"].replace({
    "It": "IT",
    "Hr": "HR"
})

# 6. Remove duplicate records
df = df.drop_duplicates()

# 7. Detect outliers using IQR
print("\nOUTLIER DETECTION")

for col in ["age", "experience_years", "salary_inr"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    print(f"{col}: {len(outliers)} outliers")

# Keep outliers because unusual values may be genuine
# employee records. Do not delete without verification.

# 8. After cleaning summary
after_rows = len(df)
after_missing = int(df.isnull().sum().sum())
after_duplicates = int(df.duplicated().sum())

summary = pd.DataFrame({
    "Metric": ["Rows", "Missing Values", "Duplicates"],
    "Before": [before_rows, before_missing, before_duplicates],
    "After": [after_rows, after_missing, after_duplicates]
})

print("\nBEFORE AND AFTER SUMMARY")
print(summary)

# 9. Save cleaned dataset and summary
df.to_csv("clean_data.csv", index=False)
summary.to_csv("cleaning_summary.csv", index=False)

print("\nCleaning completed successfully!")
print("Files saved: clean_data.csv and cleaning_summary.csv")