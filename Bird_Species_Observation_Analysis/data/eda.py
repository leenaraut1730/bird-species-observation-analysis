import pandas as pd

# ============================================
# 1. Load Cleaned Dataset
# ============================================

file_path = "data/bird_observation_cleaned.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET INFORMATION ==========")

print("Shape:", df.shape)


# ============================================
# 2. Total Observations
# ============================================

print("\n========== TOTAL OBSERVATIONS ==========")

print("Total observations:", len(df))


# ============================================
# 3. Unique Species
# ============================================

print("\n========== SPECIES ANALYSIS ==========")

unique_species = df["Scientific_Name"].nunique()

print("Unique scientific species:", unique_species)

unique_common_names = df["Common_Name"].nunique()

print("Unique common bird names:", unique_common_names)


# ============================================
# 4. Habitat Distribution
# ============================================

print("\n========== HABITAT ANALYSIS ==========")

habitat_counts = df["Habitat"].value_counts()

print(habitat_counts)


# ============================================
# 5. Species Observations
# ============================================

print("\n========== TOP 10 SPECIES ==========")

top_species = (
    df["Common_Name"]
    .value_counts()
    .head(10)
)

print(top_species)


# ============================================
# 6. Scientific Species
# ============================================

print("\n========== TOP 10 SCIENTIFIC SPECIES ==========")

top_scientific = (
    df["Scientific_Name"]
    .value_counts()
    .head(10)
)

print(top_scientific)


# ============================================
# 7. Administrative Unit Analysis
# ============================================

print("\n========== TOP ADMINISTRATIVE UNITS ==========")

admin_units = (
    df["Admin_Unit_Code"]
    .value_counts()
)

print(admin_units)


# ============================================
# 8. Site Analysis
# ============================================

print("\n========== TOP 10 SITES ==========")

top_sites = (
    df["Site_Name"]
    .value_counts()
    .head(10)
)

print(top_sites)


# ============================================
# 9. Plot Analysis
# ============================================

print("\n========== TOP 10 PLOTS ==========")

top_plots = (
    df["Plot_Name"]
    .value_counts()
    .head(10)
)

print(top_plots)


# ============================================
# 10. Year Analysis
# ============================================

print("\n========== YEAR ANALYSIS ==========")

print(
    df["Year"].value_counts().sort_index()
)


# ============================================
# 11. Month Analysis
# ============================================

print("\n========== MONTH ANALYSIS ==========")

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Month"] = df["Date"].dt.month

month_counts = (
    df["Month"]
    .value_counts()
    .sort_index()
)

print(month_counts)


# ============================================
# 12. Observer Analysis
# ============================================

print("\n========== OBSERVER ANALYSIS ==========")

top_observers = (
    df["Observer"]
    .value_counts()
    .head(10)
)

print(top_observers)


# ============================================
# 13. Identification Method
# ============================================

print("\n========== IDENTIFICATION METHOD ==========")

print(
    df["ID_Method"].value_counts()
)


# ============================================
# 14. Sex Analysis
# ============================================

print("\n========== SEX DISTRIBUTION ==========")

print(
    df["Sex"].value_counts()
)


# ============================================
# 15. Flyover Analysis
# ============================================

print("\n========== FLYOVER OBSERVATION ==========")

print(
    df["Flyover_Observed"].value_counts()
)


# ============================================
# 16. Conservation Analysis
# ============================================

print("\n========== CONSERVATION ANALYSIS ==========")

print("\nPIF Watchlist:")

print(
    df["PIF_Watchlist_Status"].value_counts()
)

print("\nRegional Stewardship:")

print(
    df["Regional_Stewardship_Status"].value_counts()
)


# ============================================
# 17. Environmental Analysis
# ============================================

print("\n========== ENVIRONMENTAL SUMMARY ==========")

print(
    df[
        [
            "Temperature",
            "Humidity"
        ]
    ].describe()
)


# ============================================
# 18. Weather Conditions
# ============================================

print("\n========== SKY CONDITIONS ==========")

print(
    df["Sky"].value_counts().head(10)
)

print("\n========== WIND CONDITIONS ==========")

print(
    df["Wind"].value_counts().head(10)
)


# ============================================
# 19. Distance Analysis
# ============================================

print("\n========== DISTANCE ANALYSIS ==========")

print(
    df["Distance"].value_counts()
)


# ============================================
# 20. Final Message
# ============================================

print("\n============================================")
print("EDA BASIC ANALYSIS COMPLETED")
print("============================================")