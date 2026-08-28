import pandas as pd
import plotly.express as px
import os

# ============================================
# 1. Load Dataset
# ============================================

df = pd.read_csv(
    "data/bird_observation_cleaned.csv"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Month"] = df["Date"].dt.month

month_names = {
    5: "May",
    6: "June",
    7: "July"
}

df["Month_Name"] = df["Month"].map(month_names)


# ============================================
# 2. Create Images Folder
# ============================================

os.makedirs("images", exist_ok=True)


# ============================================
# CHART 1 — Habitat Distribution
# ============================================

habitat = df["Habitat"].value_counts().reset_index()

habitat.columns = [
    "Habitat",
    "Observations"
]

fig = px.bar(
    habitat,
    x="Habitat",
    y="Observations",
    title="Bird Observations by Habitat",
    text="Observations"
)

fig.update_traces(
    textposition="outside"
)

fig.write_html(
    "images/habitat_distribution.html"
)

fig.show()


# ============================================
# CHART 2 — Top 10 Bird Species
# ============================================

top_species = (
    df["Common_Name"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_species.columns = [
    "Common_Name",
    "Observations"
]

fig = px.bar(
    top_species.sort_values("Observations"),
    x="Observations",
    y="Common_Name",
    orientation="h",
    title="Top 10 Most Observed Bird Species",
    text="Observations"
)

fig.update_traces(
    textposition="outside"
)

fig.write_html(
    "images/top_10_species.html"
)

fig.show()


# ============================================
# CHART 3 — Monthly Observations
# ============================================

monthly = (
    df.groupby(
        ["Month", "Month_Name"]
    )
    .size()
    .reset_index(
        name="Observations"
    )
    .sort_values("Month")
)

fig = px.line(
    monthly,
    x="Month_Name",
    y="Observations",
    markers=True,
    title="Bird Observations by Month",
    text="Observations"
)

fig.update_traces(
    textposition="top center"
)

fig.write_html(
    "images/monthly_observations.html"
)

fig.show()


# ============================================
# CHART 4 — Habitat vs Species
# ============================================

habitat_species = (
    df.groupby("Habitat")["Common_Name"]
    .nunique()
    .reset_index()
)

habitat_species.columns = [
    "Habitat",
    "Unique_Species"
]

fig = px.bar(
    habitat_species,
    x="Habitat",
    y="Unique_Species",
    title="Unique Bird Species by Habitat",
    text="Unique_Species"
)

fig.update_traces(
    textposition="outside"
)

fig.write_html(
    "images/species_by_habitat.html"
)

fig.show()


# ============================================
# CHART 5 — Identification Method
# ============================================

method = (
    df["ID_Method"]
    .value_counts()
    .reset_index()
)

method.columns = [
    "ID_Method",
    "Observations"
]

fig = px.pie(
    method,
    names="ID_Method",
    values="Observations",
    title="Bird Identification Methods",
    hole=0.45
)

fig.write_html(
    "images/identification_methods.html"
)

fig.show()


# ============================================
# CHART 6 — Sex Distribution
# ============================================

sex = (
    df["Sex"]
    .value_counts()
    .reset_index()
)

sex.columns = [
    "Sex",
    "Observations"
]

fig = px.bar(
    sex,
    x="Sex",
    y="Observations",
    title="Bird Sex Distribution",
    text="Observations"
)

fig.update_traces(
    textposition="outside"
)

fig.write_html(
    "images/sex_distribution.html"
)

fig.show()


# ============================================
# CHART 7 — Temperature Distribution
# ============================================

fig = px.histogram(
    df,
    x="Temperature",
    nbins=30,
    title="Temperature Distribution",
    labels={
        "Temperature": "Temperature (°C)"
    }
)

fig.write_html(
    "images/temperature_distribution.html"
)

fig.show()


# ============================================
# CHART 8 — Humidity Distribution
# ============================================

fig = px.histogram(
    df,
    x="Humidity",
    nbins=30,
    title="Humidity Distribution",
    labels={
        "Humidity": "Humidity (%)"
    }
)

fig.write_html(
    "images/humidity_distribution.html"
)

fig.show()


# ============================================
# CHART 9 — Conservation Status
# ============================================

conservation = pd.DataFrame({
    "Status": [
        "PIF Watchlist",
        "Regional Stewardship"
    ],
    "Yes": [
        df["PIF_Watchlist_Status"].sum(),
        df["Regional_Stewardship_Status"].sum()
    ]
})

fig = px.bar(
    conservation,
    x="Status",
    y="Yes",
    title="Conservation Status Observations",
    text="Yes"
)

fig.update_traces(
    textposition="outside"
)

fig.write_html(
    "images/conservation_status.html"
)

fig.show()


# ============================================
# CHART 10 — Habitat × ID Method
# ============================================

habitat_method = (
    df.groupby(
        ["Habitat", "ID_Method"]
    )
    .size()
    .reset_index(
        name="Observations"
    )
)

fig = px.bar(
    habitat_method,
    x="Habitat",
    y="Observations",
    color="ID_Method",
    barmode="group",
    title="Identification Method by Habitat"
)

fig.write_html(
    "images/habitat_id_method.html"
)

fig.show()


print("\n============================================")
print("ALL EDA VISUALIZATIONS CREATED SUCCESSFULLY")
print("Check the images folder.")
print("============================================")