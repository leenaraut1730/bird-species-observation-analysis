import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bird Species Observation Analysis",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: white;
    }

    .title-box {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(
            135deg,
            #12372A,
            #436850
        );
        margin-bottom: 25px;
    }

    .title-box h1 {
        color: white;
        margin-bottom: 5px;
    }

    .title-box p {
        color: #d8f3dc;
        font-size: 16px;
    }

    .kpi-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #161b22;
        border: 1px solid #30363d;
        text-align: center;
        min-height: 130px;
    }

    .kpi-title {
        color: #9da7b3;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: white;
        font-size: 30px;
        font-weight: bold;
    }

    .section-title {
        padding: 10px 0;
        border-bottom: 1px solid #30363d;
        margin-bottom: 20px;
    }

    .info-box {
        padding: 18px;
        border-radius: 12px;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #d8dee9;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    possible_paths = [
        base_dir / "data" / "bird_observation_cleaned.csv",
        base_dir / "Bird_Species_Observation_Analysis" / "data" / "bird_observation_cleaned.csv",
    ]

    file_path = None

    for path in possible_paths:
        if path.exists():
            file_path = path
            break

    if file_path is None:
        return None

    try:
        df = pd.read_csv(file_path)

        # Date conversion
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce"
            )

            df["Month"] = df["Date"].dt.month

            df["Month_Name"] = df["Date"].dt.month_name()

        # Fill important categorical columns
        categorical_columns = [
            "Habitat",
            "Common_Name",
            "Scientific_Name",
            "Admin_Unit_Code",
            "Site_Name",
            "Plot_Name",
            "ID_Method",
            "Sex",
            "Distance",
            "Sky",
            "Wind"
        ]

        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].fillna("Unknown").astype(str)

        # Boolean conversion
        boolean_columns = [
            "Flyover_Observed",
            "PIF_Watchlist_Status",
            "Regional_Stewardship_Status"
        ]

        for col in boolean_columns:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .map({
                        "true": True,
                        "false": False,
                        "yes": True,
                        "no": False,
                        "1": True,
                        "0": False
                    })
                    .fillna(False)
                )

        return df

    except Exception as e:
        st.error(f"Error while reading dataset: {e}")
        return None


df = load_data()


# ============================================================
# DATA CHECK
# ============================================================

if df is None:

    st.error(
        "❌ Dataset not found."
    )

    st.info(
        "Please keep your CSV file at:\n\n"
        "`data/bird_observation_cleaned.csv`"
    )

    st.stop()


if df.empty:

    st.error("❌ Dataset is empty.")
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="title-box">

<h1>🐦 Bird Species Observation Analysis</h1>

<p>
Explore bird observations across Forest and Grassland habitats,
species diversity, environmental conditions and conservation indicators.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🐦 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Dashboard",
        "🐦 Species Analysis",
        "🌳 Habitat & Environment",
        "🛡️ Conservation",
        "💼 Business Insights",
        "📋 Data Explorer",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("🔎 Filters")


# Habitat Filter
if "Habitat" in df.columns:

    habitat_values = sorted(
        df["Habitat"].dropna().unique().tolist()
    )

    selected_habitat = st.sidebar.multiselect(
        "Habitat",
        habitat_values,
        default=habitat_values
    )

else:
    selected_habitat = []


# Admin Unit Filter
if "Admin_Unit_Code" in df.columns:

    admin_values = sorted(
        df["Admin_Unit_Code"].dropna().unique().tolist()
    )

    selected_admin = st.sidebar.multiselect(
        "Admin Unit",
        admin_values,
        default=admin_values
    )

else:
    selected_admin = []


# ID Method Filter
if "ID_Method" in df.columns:

    id_values = sorted(
        df["ID_Method"].dropna().unique().tolist()
    )

    selected_id = st.sidebar.multiselect(
        "Identification Method",
        id_values,
        default=id_values
    )

else:
    selected_id = []


# Sex Filter
if "Sex" in df.columns:

    sex_values = sorted(
        df["Sex"].dropna().unique().tolist()
    )

    selected_sex = st.sidebar.multiselect(
        "Sex",
        sex_values,
        default=sex_values
    )

else:
    selected_sex = []


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if "Habitat" in filtered_df.columns and selected_habitat:
    filtered_df = filtered_df[
        filtered_df["Habitat"].isin(selected_habitat)
    ]


if "Admin_Unit_Code" in filtered_df.columns and selected_admin:
    filtered_df = filtered_df[
        filtered_df["Admin_Unit_Code"].isin(selected_admin)
    ]


if "ID_Method" in filtered_df.columns and selected_id:
    filtered_df = filtered_df[
        filtered_df["ID_Method"].isin(selected_id)
    ]


if "Sex" in filtered_df.columns and selected_sex:
    filtered_df = filtered_df[
        filtered_df["Sex"].isin(selected_sex)
    ]


# ============================================================
# EMPTY FILTER RESULT
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No records match the selected filters."
    )

    st.stop()


# ============================================================
# PAGE 1 - DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<h2 class="section-title">📊 Dashboard Overview</h2>',
        unsafe_allow_html=True
    )

    total_observations = len(filtered_df)

    if "Common_Name" in filtered_df.columns:
        total_species = filtered_df["Common_Name"].nunique()
    else:
        total_species = 0

    if "Habitat" in filtered_df.columns:
        total_habitats = filtered_df["Habitat"].nunique()
    else:
        total_habitats = 0

    if "Site_Name" in filtered_df.columns:
        total_sites = filtered_df["Site_Name"].nunique()
    else:
        total_sites = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Observations</div>
            <div class="kpi-value">{total_observations:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Unique Species</div>
            <div class="kpi-value">{total_species:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Habitats</div>
            <div class="kpi-value">{total_habitats:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Observation Sites</div>
            <div class="kpi-value">{total_sites:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # --------------------------------------------------------
    # Habitat Distribution
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🌳 Observations by Habitat")

        if "Habitat" in filtered_df.columns:

            habitat_count = (
                filtered_df["Habitat"]
                .value_counts()
                .reset_index()
            )

            habitat_count.columns = [
                "Habitat",
                "Observations"
            ]

            fig = px.bar(
                habitat_count,
                x="Habitat",
                y="Observations",
                title="Habitat Distribution",
                text_auto=True
            )

            fig.update_layout(
                template="plotly_dark",
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        st.subheader("🐦 Top 10 Bird Species")

        if "Common_Name" in filtered_df.columns:

            top_species = (
                filtered_df["Common_Name"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            top_species.columns = [
                "Species",
                "Observations"
            ]

            fig = px.bar(
                top_species.sort_values("Observations"),
                x="Observations",
                y="Species",
                orientation="h",
                title="Most Observed Bird Species",
                text_auto=True
            )

            fig.update_layout(
                template="plotly_dark",
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # Sex Distribution
    # --------------------------------------------------------

    if "Sex" in filtered_df.columns:

        st.subheader("👤 Sex Distribution")

        sex_data = (
            filtered_df["Sex"]
            .value_counts()
            .reset_index()
        )

        sex_data.columns = [
            "Sex",
            "Observations"
        ]

        fig = px.pie(
            sex_data,
            names="Sex",
            values="Observations",
            hole=0.45,
            title="Bird Observation by Sex"
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 2 - SPECIES ANALYSIS
# ============================================================

elif page == "🐦 Species Analysis":

    st.markdown(
        '<h2 class="section-title">🐦 Species Analysis</h2>',
        unsafe_allow_html=True
    )

    if "Common_Name" not in filtered_df.columns:

        st.warning("Common_Name column is not available.")
        st.stop()

    species_counts = (
        filtered_df["Common_Name"]
        .value_counts()
        .reset_index()
    )

    species_counts.columns = [
        "Species",
        "Observations"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top 15 Species")

        top15 = species_counts.head(15)

        fig = px.bar(
            top15.sort_values("Observations"),
            x="Observations",
            y="Species",
            orientation="h",
            title="Top 15 Most Observed Species",
            text_auto=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Species Distribution")

        fig = px.histogram(
            species_counts,
            x="Observations",
            nbins=20,
            title="Distribution of Species Observation Counts"
        )

        fig.update_layout(
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("🔍 Species Search")

    species_list = sorted(
        filtered_df["Common_Name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_species = st.selectbox(
        "Select a bird species",
        species_list
    )

    species_df = filtered_df[
        filtered_df["Common_Name"] == selected_species
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Observations",
            f"{len(species_df):,}"
        )

    with col2:
        if "Habitat" in species_df.columns:
            st.metric(
                "Habitats",
                species_df["Habitat"].nunique()
            )

    with col3:
        if "Site_Name" in species_df.columns:
            st.metric(
                "Sites",
                species_df["Site_Name"].nunique()
            )

    st.dataframe(
        species_df.head(100),
        use_container_width=True
    )


# ============================================================
# PAGE 3 - HABITAT & ENVIRONMENT
# ============================================================

elif page == "🌳 Habitat & Environment":

    st.markdown(
        '<h2 class="section-title">🌳 Habitat & Environment</h2>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Habitat
    with col1:

        if "Habitat" in filtered_df.columns:

            habitat_data = (
                filtered_df["Habitat"]
                .value_counts()
                .reset_index()
            )

            habitat_data.columns = [
                "Habitat",
                "Observations"
            ]

            fig = px.pie(
                habitat_data,
                names="Habitat",
                values="Observations",
                hole=0.4,
                title="Habitat Composition"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Distance
    with col2:

        if "Distance" in filtered_df.columns:

            distance_data = (
                filtered_df["Distance"]
                .value_counts()
                .reset_index()
            )

            distance_data.columns = [
                "Distance",
                "Observations"
            ]

            fig = px.bar(
                distance_data,
                x="Distance",
                y="Observations",
                title="Observation Distance"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Weather
    if "Sky" in filtered_df.columns:

        st.subheader("☁️ Sky Conditions")

        sky_data = (
            filtered_df["Sky"]
            .value_counts()
            .reset_index()
        )

        sky_data.columns = [
            "Sky",
            "Observations"
        ]

        fig = px.bar(
            sky_data,
            x="Sky",
            y="Observations",
            title="Observations by Sky Condition",
            text_auto=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Wind
    if "Wind" in filtered_df.columns:

        st.subheader("💨 Wind Conditions")

        wind_data = (
            filtered_df["Wind"]
            .value_counts()
            .reset_index()
        )

        wind_data.columns = [
            "Wind",
            "Observations"
        ]

        fig = px.bar(
            wind_data,
            x="Wind",
            y="Observations",
            title="Observations by Wind Condition",
            text_auto=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 4 - CONSERVATION
# ============================================================

elif page == "🛡️ Conservation":

    st.markdown(
        '<h2 class="section-title">🛡️ Conservation Analysis</h2>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Watchlist
    with col1:

        if "PIF_Watchlist_Status" in filtered_df.columns:

            watchlist = (
                filtered_df["PIF_Watchlist_Status"]
                .value_counts()
                .reset_index()
            )

            watchlist.columns = [
                "Status",
                "Observations"
            ]

            fig = px.pie(
                watchlist,
                names="Status",
                values="Observations",
                hole=0.4,
                title="PIF Watchlist Status"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Stewardship
    with col2:

        if "Regional_Stewardship_Status" in filtered_df.columns:

            stewardship = (
                filtered_df["Regional_Stewardship_Status"]
                .value_counts()
                .reset_index()
            )

            stewardship.columns = [
                "Status",
                "Observations"
            ]

            fig = px.pie(
                stewardship,
                names="Status",
                values="Observations",
                hole=0.4,
                title="Regional Stewardship Status"
            )

            fig.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Flyover
    if "Flyover_Observed" in filtered_df.columns:

        st.subheader("🪽 Flyover Observations")

        flyover = (
            filtered_df["Flyover_Observed"]
            .value_counts()
            .reset_index()
        )

        flyover.columns = [
            "Flyover Observed",
            "Observations"
        ]

        fig = px.bar(
            flyover,
            x="Flyover Observed",
            y="Observations",
            title="Flyover Observation Status",
            text_auto=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 5 - DATA EXPLORER
# ============================================================

elif page == "📋 Data Explorer":

    st.markdown(
        '<h2 class="section-title">📋 Data Explorer</h2>',
        unsafe_allow_html=True
    )

    st.write(
        f"Showing **{len(filtered_df):,}** filtered records."
    )

    # Search
    search_text = st.text_input(
        "🔎 Search bird species"
    )

    display_df = filtered_df.copy()

    if search_text and "Common_Name" in display_df.columns:

        display_df = display_df[
            display_df["Common_Name"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600
    )

    # Download
    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="filtered_bird_observations.csv",
        mime="text/csv"
    )
# ============================================================
# PAGE 5 - BUSINESS INSIGHTS & RECOMMENDATIONS
# ============================================================

elif page == "💼 Business Insights":

    st.markdown(
        '<h2 class="section-title">💼 Business Insights & Recommendations</h2>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-box">

    <h3>🎯 Decision Support</h3>

    <p>
    This section converts bird observation data into actionable
    insights and recommendations for habitat management,
    conservation planning, field monitoring and future surveys.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ========================================================
    # CALCULATE INSIGHTS
    # ========================================================

    total_records = len(filtered_df)

    if "Common_Name" in filtered_df.columns:
        species_count = filtered_df["Common_Name"].nunique()
        species_frequency = filtered_df["Common_Name"].value_counts()

        top_species = species_frequency.index[0]
        top_species_count = species_frequency.iloc[0]

    else:
        species_count = 0
        top_species = "N/A"
        top_species_count = 0

    if "Habitat" in filtered_df.columns:

        habitat_frequency = (
            filtered_df["Habitat"]
            .value_counts()
        )

        top_habitat = habitat_frequency.index[0]
        top_habitat_count = habitat_frequency.iloc[0]

    else:

        top_habitat = "N/A"
        top_habitat_count = 0

    if "Site_Name" in filtered_df.columns:

        site_count = filtered_df["Site_Name"].nunique()

    else:

        site_count = 0

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Species Observed</div>
            <div class="kpi-value">{species_count:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Species</div>
            <div class="kpi-value" style="font-size:20px;">
                {top_species}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Dominant Habitat</div>
            <div class="kpi-value" style="font-size:22px;">
                {top_habitat}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Monitoring Sites</div>
            <div class="kpi-value">{site_count:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    st.subheader("🔍 Key Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.markdown(f"""
        <div class="info-box">

        <h4>🐦 Species Diversity</h4>

        <p>
        The filtered dataset contains <b>{species_count}</b>
        unique bird species across <b>{total_records:,}</b>
        observations.
        </p>

        <p>
        The most frequently observed species is
        <b>{top_species}</b>, with
        <b>{top_species_count:,}</b> observations.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with insight_col2:

        st.markdown(f"""
        <div class="info-box">

        <h4>🌳 Habitat Concentration</h4>

        <p>
        <b>{top_habitat}</b> is currently the habitat with
        the highest number of observations.
        </p>

        <p>
        It contains approximately
        <b>{top_habitat_count:,}</b> observations
        in the selected dataset.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ========================================================
    # HABITAT PERFORMANCE
    # ========================================================

    if "Habitat" in filtered_df.columns:

        st.subheader("📊 Habitat Observation Performance")

        habitat_data = (
            filtered_df["Habitat"]
            .value_counts()
            .reset_index()
        )

        habitat_data.columns = [
            "Habitat",
            "Observations"
        ]

        habitat_data["Percentage"] = (
            habitat_data["Observations"]
            / habitat_data["Observations"].sum()
            * 100
        ).round(2)

        fig = px.bar(
            habitat_data,
            x="Habitat",
            y="Observations",
            text="Percentage",
            title="Observation Distribution by Habitat"
        )

        fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # TOP SPECIES BUSINESS VALUE
    # ========================================================

    if "Common_Name" in filtered_df.columns:

        st.subheader("🏆 Priority Species")

        top_species_df = (
            filtered_df["Common_Name"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_species_df.columns = [
            "Species",
            "Observations"
        ]

        fig = px.bar(
            top_species_df.sort_values("Observations"),
            x="Observations",
            y="Species",
            orientation="h",
            title="Top 10 Species for Monitoring Priority",
            text_auto=True
        )

        fig.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.subheader("💡 Recommendations")

    recommendations = [
        (
            "🌳 Habitat Management",
            f"Prioritize monitoring and habitat management activities "
            f"in {top_habitat}, which currently has the highest number "
            f"of observations."
        ),

        (
            "🐦 Species Monitoring",
            f"Continue regular monitoring of {top_species}, "
            f"the most frequently observed species in the filtered data."
        ),

        (
            "📍 Site-Level Monitoring",
            "Compare observation counts across monitoring sites "
            "to identify locations requiring additional field surveys."
        ),

        (
            "🌦️ Environmental Monitoring",
            "Combine bird observations with temperature, humidity, "
            "sky and wind conditions to understand environmental "
            "patterns associated with bird activity."
        ),

        (
            "🛡️ Conservation Planning",
            "Use conservation-status indicators to prioritize "
            "species and habitats that may require additional "
            "monitoring or protection."
        ),

        (
            "📅 Long-Term Tracking",
            "Maintain consistent observations over multiple years "
            "to identify changes in species occurrence and habitat use."
        )
    ]

    for title, recommendation in recommendations:

        st.markdown(
            f"""
            <div class="info-box" style="margin-bottom:12px;">

            <h4>{title}</h4>

            <p>{recommendation}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # MANAGEMENT ACTION PLAN
    # ========================================================

    st.subheader("🚀 Recommended Action Plan")

    action_data = pd.DataFrame({
        "Priority": [
            "High",
            "High",
            "Medium",
            "Medium",
            "Low"
        ],

        "Action": [
            "Protect important habitats",
            "Monitor priority species",
            "Increase site-level surveys",
            "Track environmental conditions",
            "Perform long-term trend analysis"
        ],

        "Expected Outcome": [
            "Improved habitat protection",
            "Better conservation monitoring",
            "Improved observation coverage",
            "Better understanding of bird activity",
            "Identification of population trends"
        ]
    })

    st.dataframe(
        action_data,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    st.subheader("📌 Executive Summary")

    st.markdown(f"""
    <div class="info-box">

    <p>
    Based on the currently selected filters, the analysis covers
    <b>{total_records:,}</b> bird observations representing
    <b>{species_count}</b> species across
    <b>{site_count}</b> monitoring sites.
    </p>

    <p>
    <b>{top_species}</b> is the most frequently observed species,
    while <b>{top_habitat}</b> represents the habitat with the
    highest observation volume.
    </p>

    <p>
    The recommended strategy is to prioritize habitat protection,
    continue species-level monitoring, improve field coverage,
    integrate environmental observations and perform long-term
    trend analysis.
    </p>

    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE 6 - ABOUT
# ============================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<h2 class="section-title">ℹ️ About the Project</h2>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-box">

    <h3>🐦 Bird Species Observation Analysis</h3>

    <p>
    This project analyzes bird observations collected from
    different habitats, with a focus on Forest and Grassland
    environments.
    </p>

    <h4>🎯 Project Objectives</h4>

    <ul>
        <li>Analyze bird species observations</li>
        <li>Compare different habitats</li>
        <li>Identify commonly observed species</li>
        <li>Analyze environmental conditions</li>
        <li>Explore conservation indicators</li>
        <li>Provide an interactive dashboard</li>
    </ul>

    <h4>🛠️ Technologies Used</h4>

    <ul>
        <li>Python</li>
        <li>Pandas</li>
        <li>NumPy</li>
        <li>Plotly</li>
        <li>Streamlit</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <center>
    <small>
    🐦 Bird Species Observation Analysis |
    Interactive Data Analytics Dashboard
    </small>
    </center>
    """,
    unsafe_allow_html=True
)
