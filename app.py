import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Page title
st.title("AI Prototype: AFC Transformation Operationalization & Transition Intelligence Platform")

st.write("""
This prototype explores AI-driven transition readiness,
governance operationalization and BAU sustainment intelligence
across AFC and compliance transformation programs.
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload AFC Transformation Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Transformation Dataset")

    st.dataframe(df)

    findings = []

    # Readiness analysis
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # Governance ownership
        if row["owner_assigned"] == "no":
            risk_score += 25
            issues.append("Missing ownership")

        # SOP readiness
        if row["sop_complete"] == "no":
            risk_score += 20
            issues.append("Incomplete SOPs")

        # Support model
        if row["support_model_ready"] == "no":
            risk_score += 20
            issues.append("Support model not ready")

        # Open remediation
        if row["open_issues"] > 3:
            risk_score += 20
            issues.append("High remediation backlog")

        # BAU readiness
        if row["bau_ready"] == "no":
            risk_score += 30
            issues.append("Not BAU ready")

        # Regulatory exposure
        if row["regulatory_criticality"] == "high":
            risk_score += 25
            issues.append("High regulatory exposure")

        # Readiness status
        readiness_status = "Not Ready"

        if risk_score < 40:
            readiness_status = "Ready"

        elif risk_score < 70:
            readiness_status = "Partially Ready"

        findings.append({
            "workstream": row["workstream"],
            "risk_score": risk_score,
            "issues": ", ".join(issues),
            "transition_status": readiness_status
        })

    risk_df = pd.DataFrame(findings)

    # Stateful data
    if "transition_data" not in st.session_state:
        st.session_state.transition_data = risk_df.copy()

    transition_df = st.session_state.transition_data

    # Metrics
    st.subheader("Transition Readiness Metrics")

    readiness_score = 100 - int(
        transition_df["risk_score"].mean()
    )

    ready_count = len(
        transition_df[
            transition_df["transition_status"] == "Ready"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Transition Readiness Score",
            f"{readiness_score}/100"
        )

    with col2:
        st.metric(
            "BAU Ready Workstreams",
            ready_count
        )

    # Chart
    st.subheader("Transition Risk Distribution")

    st.bar_chart(
        transition_df.set_index("workstream")["risk_score"]
    )

    # Findings
    st.subheader("Transition Readiness Findings")

    st.dataframe(transition_df)

    # Workflow actions
    st.subheader("Operationalization Actions")

    selected_workstream = st.selectbox(
        "Select Workstream",
        transition_df["workstream"]
    )

    action = st.selectbox(
        "Select Action",
        [
            "Assign Governance Owner",
            "Complete SOP",
            "Enable Support Model",
            "Close Remediation Issues",
            "Approve BAU Transition"
        ]
    )

    if st.button("Execute Action"):

        current_score = transition_df.loc[
            transition_df["workstream"] == selected_workstream,
            "risk_score"
        ].values[0]

        # Governance owner
        if action == "Assign Governance Owner":

            new_score = max(current_score - 15, 0)

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "risk_score"
            ] = new_score

        # SOP completion
        elif action == "Complete SOP":

            new_score = max(current_score - 15, 0)

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "risk_score"
            ] = new_score

        # Support model
        elif action == "Enable Support Model":

            new_score = max(current_score - 15, 0)

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "risk_score"
            ] = new_score

        # Close remediation
        elif action == "Close Remediation Issues":

            new_score = max(current_score - 20, 0)

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "risk_score"
            ] = new_score

        # Approve BAU
        elif action == "Approve BAU Transition":

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "risk_score"
            ] = 0

            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "issues"
            ] = "Transition Complete"

        # Refresh transition readiness
        updated_score = transition_df.loc[
            transition_df["workstream"] == selected_workstream,
            "risk_score"
        ].values[0]

        if updated_score < 40:
            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "transition_status"
            ] = "Ready"

        elif updated_score < 70:
            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "transition_status"
            ] = "Partially Ready"

        else:
            transition_df.loc[
                transition_df["workstream"] == selected_workstream,
                "transition_status"
            ] = "Not Ready"

        st.success(
            f"{action} executed successfully for {selected_workstream}"
        )

    # Updated posture
    st.subheader("Updated Transition Readiness")

    st.dataframe(transition_df)

    # Download updated CSV
    csv = transition_df.to_csv(index=False)

    st.download_button(
        label="Download Updated Transition Dataset",
        data=csv,
        file_name="updated_transition_dataset.csv",
        mime="text/csv"
    )

    # AI Operationalization Insights
    st.subheader("AI Operationalization Intelligence")

    summary = transition_df.to_string(index=False)

    prompt = f"""
    Analyze the following AFC transformation transition findings.

    Identify:
    - governance readiness gaps
    - BAU transition blockers
    - operationalization weaknesses
    - sustainment risks
    - unresolved dependencies

    Recommend:
    - readiness actions
    - governance operationalization steps
    - proposed BAU operating model
    - governance forums
    - ownership structure
    - transition execution plan

    Findings:
    {summary}
    """

    with st.spinner("Generating AI operationalization insights..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior AFC transformation operationalization and governance transition expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content

        st.write(output)
