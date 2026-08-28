import pandas as pd
import os

# ============================================
# 1. Load Master Dataset
# ============================================

input_file = "data/bird_observation_master.csv"

df = pd.read_csv(input_file)

print("Original Shape:", df.shape)


# ============================================
# 2. Convert Date
# ============================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


# ============================================
# 3. Remove Exact Duplicate Rows
# ============================================

before_duplicates = len(df)

df = df.drop_duplicates().reset_index(drop=True)

after_duplicates = len(df)

print("\n========== DUPLICATE CLEANING ==========")
print("Before:", before_duplicates)
print("After:", after_duplicates)
print("Removed:", before_duplicates - after_duplicates)


# ============================================
# 4. Handle Missing Categorical Values
# ============================================

df["Sex"] = df["Sex"].fillna("Unknown")

df["Distance"] = df["Distance"].fillna("Unknown")

df["ID_Method"] = df["ID_Method"].fillna("Unknown")


# ============================================
# 5. Drop Highly Missing Column
# ============================================

df = df.drop(
    columns=["Sub_Unit_Code"],
    errors="ignore"
)


# ============================================
# 6. Remove Completely Unnecessary Duplicate
# ============================================

# Location_Type and Habitat contain the same information.
# Keep Habitat because it is useful for analysis.

if "Location_Type" in df.columns:
    df = df.drop(columns=["Location_Type"])


# ============================================
# 7. Check Missing Values Again
# ============================================

print("\n========== MISSING VALUES AFTER CLEANING ==========")

missing = df.isnull().sum()

missing_report = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": (
        df.isnull().mean() * 100
    ).round(2)
})

print(
    missing_report[
        missing_report["Missing_Count"] > 0
    ].sort_values(
        "Missing_Count",
        ascending=False
    )
)


# ============================================
# 8. Check Duplicate Rows Again
# ============================================

print("\n========== DUPLICATE CHECK ==========")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)


# ============================================
# 9. Final Dataset Information
# ============================================

print("\n========== FINAL DATASET ==========")

print("Shape:", df.shape)

print("\nHabitat:")
print(df["Habitat"].value_counts())

print("\nSex:")
print(df["Sex"].value_counts())

print("\nDistance:")
print(df["Distance"].value_counts())

print("\nID Method:")
print(df["ID_Method"].value_counts())


# ============================================
# 10. Save Cleaned Dataset
# ============================================

output_file = "data/bird_observation_cleaned.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n============================================")
print("CLEANED DATASET CREATED SUCCESSFULLY")
print("Saved:", output_file)
print("Final Shape:", df.shape)
print("============================================")