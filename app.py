import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Medical Resources Explorer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Exploring Medical Resources Across Lebanese Towns")

st.write(
    """
    This interactive dashboard explores the availability of different
    medical resources across Lebanese towns. Use the selectors below to
    identify towns with higher availability of specific resources and
    investigate relationships between different types of medical facilities.
    """
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("heath status.csv")

# Medical resource columns
resources = {
    "Hospitals": "Type and size of medical resources - Hospitals",
    "Pharmacies": "Type and size of medical resources - Pharmacies",
    "Clinics": "Type and size of medical resources - Clinics",
    "Medical Centers": "Type and size of medical resources - Medical Centers",
    "Labs & Radiology": "Type and size of medical resources - Labs and Radiology "
}

# Convert resource columns to numeric
for column in resources.values():
    df[column] = pd.to_numeric(df[column], errors="coerce")

# --------------------------------------------------
# INTERACTION 1
# --------------------------------------------------

st.header("1. Explore Medical Resources")

selected_resource = st.selectbox(
    "Which medical resource would you like to explore?",
    list(resources.keys())
)

selected_column = resources[selected_resource]

# Prepare data for bar chart
bar_data = (
    df.groupby("Town")[selected_column]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

fig1 = px.bar(
    bar_data,
    x="Town",
    y=selected_column,
    title=f"Top 10 Towns by Number of {selected_resource}",
    labels={
        "Town": "Town",
        selected_column: f"Number of {selected_resource}"
    }
)

fig1.update_layout(
    template="plotly_white",
    xaxis_tickangle=-45
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    f"""
    **Insight:** This visualization highlights the towns with the highest
    recorded numbers of {selected_resource.lower()}. It allows the user
    to quickly identify where this type of medical resource is more concentrated.
    """
)

# --------------------------------------------------
# DESIGN JUSTIFICATION 1
# --------------------------------------------------

with st.expander("Why use this interaction?"):
    st.write(
        """
        **User question:** Which towns have the highest availability of the
        medical resource I am interested in?

        **Why a dropdown?** A dropdown is appropriate because the user needs
        to select one resource from a small predefined list. It keeps the
        interface simple and avoids displaying several separate charts at once.

        **Course concept:** This interaction reduces clutter and focuses
        attention. Instead of presenting every medical resource simultaneously,
        the visualization displays only the information relevant to the user's
        selected resource.
        """
    )

# --------------------------------------------------
# INTERACTION 2 - LINKED TO INTERACTION 1
# --------------------------------------------------

st.header("2. Compare Medical Resources")

# Remove the first selected resource from the second dropdown
comparison_options = [
    resource for resource in resources.keys()
    if resource != selected_resource
]

comparison_resource = st.selectbox(
    f"Compare {selected_resource} with:",
    comparison_options
)

comparison_column = resources[comparison_resource]

# --------------------------------------------------
# PREPARE SCATTER DATA
# --------------------------------------------------

scatter_data = df[
    ["Town", selected_column, comparison_column]
].dropna()

# --------------------------------------------------
# SCATTER PLOT
# --------------------------------------------------

fig2 = px.scatter(
    scatter_data,
    x=selected_column,
    y=comparison_column,
    hover_name="Town",
    trendline="ols",
    title=f"{selected_resource} vs. {comparison_resource} Across Towns",
    labels={
        selected_column: f"Number of {selected_resource}",
        comparison_column: f"Number of {comparison_resource}"
    }
)

fig2.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    f"""
    **Insight:** This visualization allows the user to examine whether towns
    with higher numbers of {selected_resource.lower()} also tend to have
    higher numbers of {comparison_resource.lower()}. The trend line helps
    reveal the overall direction of the relationship.
    """
)

# --------------------------------------------------
# DESIGN JUSTIFICATION 2
# --------------------------------------------------

with st.expander("Why use this comparison interaction?"):
    st.write(
        f"""
        **User question:** How is the availability of {selected_resource.lower()}
        related to another type of medical resource across towns?

        **Why a dropdown?** A dropdown is suitable because only one comparison
        variable is needed at a time. The options are linked to the first
        selector, so the selected resource is automatically removed from this
        list. This prevents the user from comparing a resource with itself.

        **Course concept:** Linking the two interactions guides the user's
        attention toward meaningful comparisons and reduces unnecessary choices.
        It provides context while allowing the user to progressively explore
        relationships in the data.
        """
    )

# --------------------------------------------------
# DATA CONTEXT
# --------------------------------------------------

st.divider()

st.subheader("About the Data")

st.write(
    """
    The dataset contains information about medical resources across Lebanese
    towns, including hospitals, pharmacies, clinics, medical centers, and
    laboratories and radiology centers.
    """
)
