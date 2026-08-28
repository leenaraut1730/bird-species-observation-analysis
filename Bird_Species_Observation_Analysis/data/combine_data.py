import pandas as pd
import os

# ============================================
# 1. File paths
# ============================================

forest_file = "data/Bird_Monitoring_Data_FOREST (2).XLSX"
grassland_file = "data/Bird_Monitoring_Data_GRASSLAND (1).XLSX"


# ============================================
# 2. Read all Excel sheets
# ============================================

forest_sheets = pd.read_excel(
    forest_file,
    sheet_name=None
)

grassland_sheets = pd.read_excel(
    grassland_file,
    sheet_name=None
)


# ============================================
# 3. Combine Forest sheets
# ============================================

forest_data = []

for sheet_name, df in forest_sheets.items():

    if not df.empty:

        df = df.copy()

        # Add habitat information
        df["Habitat"] = "Forest"

        # Keep original sheet information
        df["Source_Sheet"] = sheet_name

        forest_data.append(df)


forest_df = pd.concat(
    forest_data,
    ignore_index=True
)


# ============================================
# 4. Combine Grassland sheets
# ============================================

grassland_data = []

for sheet_name, df in grassland_sheets.items():

    if not df.empty:

        df = df.copy()

        # Add habitat information
        df["Habitat"] = "Grassland"

        # Keep original sheet information
        df["Source_Sheet"] = sheet_name

        grassland_data.append(df)


grassland_df = pd.concat(
    grassland_data,
    ignore_index=True
)


# ============================================
# 5. Combine Forest + Grassland
# ============================================

master_df = pd.concat(
    [forest_df, grassland_df],
    ignore_index=True
)


# ============================================
# 6. Display information
# ============================================

print("\n========== DATASET SUMMARY ==========")

print("Forest records:", len(forest_df))
print("Grassland records:", len(grassland_df))
print("Total records:", len(master_df))

print("\nDataset shape:")
print(master_df.shape)

print("\nHabitat distribution:")
print(master_df["Habitat"].value_counts())

print("\nColumns:")
print(master_df.columns.tolist())


# ============================================
# 7. Save Master Dataset
# ============================================

os.makedirs("data", exist_ok=True)

output_file = "data/bird_observation_master.csv"

master_df.to_csv(
    output_file,
    index=False
)

print("\n======================================")
print("Master dataset created successfully!")
print("Saved at:", output_file)
print("======================================")