import pandas as pd

# Load cleaned employee dataset
df = pd.read_csv("clean_data.csv")

print("EMPLOYEE DATASET")
print(df.head())

print("\nDATASET INFORMATION")
print(df.info())

print("\nTOTAL EMPLOYEES:", len(df))
# Step 4: Summary Statistics

numeric_columns = [
    "age",
    "experience_years",
    "salary_inr",
    "performance_rating"
]

print("\nSUMMARY STATISTICS")

summary = df[numeric_columns].agg([
    "mean",
    "median",
    "min",
    "max",
    "std"
])

print(summary)
# Step 5: GroupBy Analysis

print("\nDEPARTMENT ANALYSIS")

department_analysis = df.groupby("department").agg(
    employee_count=("employee_id", "count"),
    average_salary=("salary_inr", "mean"),
    average_age=("age", "mean")
)

print(department_analysis)

print("\nCITY ANALYSIS")

city_analysis = df.groupby("city").agg(
    employee_count=("employee_id", "count"),
    average_salary=("salary_inr", "mean")
)

print(city_analysis)

print("\nGENDER ANALYSIS")

gender_analysis = df.groupby("gender").agg(
    employee_count=("employee_id", "count"),
    average_salary=("salary_inr", "mean")
)

print(gender_analysis)
# Step 6: Correlation Analysis

print("\nCORRELATION ANALYSIS")

numeric_columns = [
    "age",
    "experience_years",
    "salary_inr",
    "performance_rating"
]

correlation = df[numeric_columns].corr()

print("\nCorrelation Matrix:")
print(correlation)

# Find top 3 correlations
correlation_pairs = correlation.unstack()

correlation_pairs = correlation_pairs[
    correlation_pairs.index.get_level_values(0) <
    correlation_pairs.index.get_level_values(1)
]

top_3 = correlation_pairs.abs().sort_values(
    ascending=False
).head(3)

print("\nTOP 3 CORRELATIONS:")
print(top_3)
print("\nBUSINESS QUESTIONS")

# 1. Which department has the highest average salary?
dept_salary = df.groupby("department")["salary_inr"].mean()
print("\n1. Department with highest average salary:")
print(dept_salary.idxmax(), "-", round(dept_salary.max(), 2))

# 2. Which city has the most employees?
city_count = df["city"].value_counts()
print("\n2. City with most employees:")
print(city_count.idxmax(), "-", city_count.max(), "employees")

# 3. What is the average salary of male and female employees?
gender_salary = df.groupby("gender")["salary_inr"].mean()
print("\n3. Average salary by gender:")
print(gender_salary)

# 4. What is the average experience of employees?
print("\n4. Average experience:")
print(round(df["experience_years"].mean(), 2), "years")

# 5. How many employees have a performance rating of 5?
high_performers = (df["performance_rating"] == 5).sum()
print("\n5. Employees with rating 5:")
print(high_performers)
print("\nMERGE ANALYSIS")

# Create a second sample table
departments = df["department"].dropna().unique()

department_data = pd.DataFrame({
    "department": departments,
    "department_code": [
        f"DEPT{i+1:03d}" for i in range(len(departments))
    ],
    "training_budget_inr": [
        50000 * (i + 1) for i in range(len(departments))
    ]
})

print("\nSECOND TABLE:")
print(department_data)

# Merge employee data with department data
merged_df = pd.merge(
    df,
    department_data,
    on="department",
    how="left"
)

print("\nMERGED DATA:")
print(merged_df.head())

print("\nMerged rows:", len(merged_df))

# Save merged data
merged_df.to_csv("merged_employee_data.csv", index=False)

print("\nMerged file saved successfully!")
print("\nBONUS CHALLENGE - PIVOT TABLE")

pivot = pd.pivot_table(
    df,
    values="salary_inr",
    index="department",
    columns="gender",
    aggfunc="mean"
)

print("\nAverage Salary by Department and Gender:")
print(pivot)

# Save pivot table
pivot.to_csv("employee_pivot_table.csv")

print("\nPivot table saved successfully!")