import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Churn & Retention",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD AND CLEAN DATA
# =========================================================

df = pd.read_csv("churn_dataset.csv")

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df = df.dropna(subset=["TotalCharges"])


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #FFFFFF;
}

h1, h2, h3 {
    color: #111111 !important;
}

p {
    color: #333333 !important;
}


/* KPI Cards */

.metric-card {
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    min-height: 105px;
}

.metric-title {
    font-size: 15px;
    margin-bottom: 8px;
    color: white !important;
}

.metric-value {
    font-size: 27px;
    font-weight: bold;
    color: white !important;
}


/* Risk Factor Cards */

.risk-card {
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    background-color: #F8FAFC;
    min-height: 115px;
}

.risk-title {
    font-size: 17px;
    font-weight: 700;
    color: #111111;
    margin-bottom: 8px;
}

.risk-value {
    font-size: 22px;
    font-weight: 700;
    color: #DC2626;
    margin-bottom: 6px;
}

.risk-description {
    font-size: 14px;
    color: #444444;
}


/* Prediction Section */

.prediction-box {
    padding: 25px;
    border-radius: 12px;
    background-color: #F8FAFC;
    border: 1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.title("Customer Churn & Retention Analysis")

st.write(
    "Identify customer segments associated with higher churn "
    "and support targeted retention decisions."
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = len(df)

churn_rate = (
    (df["Churn"] == "Yes").mean() * 100
)

avg_monthly_charges = df["MonthlyCharges"].mean()


very_high_risk_customers = (
    (df["tenure"] <= 12) &
    (df["Contract"] == "Month-to-month") &
    (df["PaymentMethod"] == "Electronic check")
).sum()


# =========================================================
# KPI CARDS
# =========================================================

st.write("")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
        <div class="metric-card" style="background-color:#2563EB;">
            <div class="metric-title">Total Customers</div>
            <div class="metric-value">{total_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="metric-card" style="background-color:#DC2626;">
            <div class="metric-title">Churn Rate</div>
            <div class="metric-value">{churn_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="metric-card" style="background-color:#059669;">
            <div class="metric-title">Average Monthly Charges</div>
            <div class="metric-value">${avg_monthly_charges:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        f"""
        <div class="metric-card" style="background-color:#7C3AED;">
            <div class="metric-title">Very High-Risk Customers</div>
            <div class="metric-value">{very_high_risk_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HIGH-RISK FACTORS
# =========================================================

st.divider()

st.header("High-Risk Factors")

st.write(
    "Customer characteristics associated with substantially higher "
    "observed churn in the dataset."
)


# First row
col1, col2 = st.columns(2)


with col1:
    st.markdown(
        """
        <div class="risk-card">

        <div class="risk-title">
        Month-to-Month Contract
        </div>

        <div class="risk-value">
        42.7% churn
        </div>

        <div class="risk-description">
        Customers on month-to-month contracts show much higher
        observed churn than customers on longer contracts.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="risk-card">

        <div class="risk-title">
        First 12 Months
        </div>

        <div class="risk-value">
        47.7% churn
        </div>

        <div class="risk-description">
        Customers in their first year have the highest observed
        churn among the tenure groups.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# Second row
col1, col2 = st.columns(2)


with col1:
    st.markdown(
        """
        <div class="risk-card">

        <div class="risk-title">
        Electronic Check
        </div>

        <div class="risk-value">
        45.3% churn
        </div>

        <div class="risk-description">
        Electronic-check customers show substantially higher
        observed churn than other payment groups.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="risk-card">

        <div class="risk-title">
        Combined High-Risk Segment 
        </div>

        <div class="risk-value">
        63.1% churn
        </div>

        <div class="risk-description">
        Customers with all three identified risk characteristics
        have the highest observed churn rate.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MODEL INSIGHTS
# =========================================================

st.divider()

st.header("Model Insights")

st.write(
    "Logistic Regression was selected as the final model after "
    "comparison with Random Forest."
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        """
        <div class="risk-card">
            <div class="risk-title">Accuracy</div>
            <div class="risk-value">80.4%</div>
            <div class="risk-description">
                Overall proportion of correct predictions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="risk-card">
            <div class="risk-title">Precision</div>
            <div class="risk-value">64.8%</div>
            <div class="risk-description">
                Proportion of predicted churners who actually churned.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        """
        <div class="risk-card">
            <div class="risk-title">Recall</div>
            <div class="risk-value">57.5%</div>
            <div class="risk-description">
                Proportion of actual churners identified by the model.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        """
        <div class="risk-card">
            <div class="risk-title">F1 Score</div>
            <div class="risk-value">60.9%</div>
            <div class="risk-description">
                Balance between precision and recall.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )