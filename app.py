import streamlit as st
from datetime import date
import pandas as pd

from database import (
    init_db,
    add_patient,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient,
    email_exists_for_other,
)
from validators import validate_all_fields, calculate_age
from ai_service import get_health_remarks

# --------------------------------------------------
# App Config
# --------------------------------------------------
st.set_page_config(
    page_title="MIRA - Health Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()


# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f4f7fb 0%, #eef4f7 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    .app-header {
        background:
            radial-gradient(circle at top right, rgba(255,255,255,0.12), transparent 30%),
            linear-gradient(135deg, #0f766e 0%, #0f5f75 48%, #164e63 100%);
        padding: 30px 34px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 18px 40px rgba(15, 118, 110, 0.18);
        position: relative;
        overflow: hidden;
    }

    .app-header::after {
        content: "";
        position: absolute;
        right: -30px;
        top: -30px;
        width: 160px;
        height: 160px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }

    .app-eyebrow {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.16);
        margin-bottom: 14px;
    }

    .app-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.3px;
        line-height: 1.15;
    }

    .app-header p {
        margin: 10px 0 0 0;
        opacity: 0.95;
        font-size: 1rem;
        max-width: 760px;
        line-height: 1.6;
    }

    .section-shell {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        backdrop-filter: blur(6px);
    }

    .section-title {
        font-size: 1.28rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
        letter-spacing: -0.2px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 0.94rem;
        margin-bottom: 16px;
        line-height: 1.5;
    }

    .sub-heading {
        font-size: 1rem;
        font-weight: 800;
        color: #334155;
        margin-bottom: 12px;
        margin-top: 6px;
    }

    .info-strip {
        background: linear-gradient(90deg, #ecfeff 0%, #f0fdfa 100%);
        border: 1px solid #b6ece4;
        color: #115e59;
        padding: 14px 16px;
        border-radius: 12px;
        font-size: 0.93rem;
        margin-top: 4px;
        margin-bottom: 14px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
    }

    .reference-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px 18px;
        min-height: 132px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
    }

    .reference-card h4 {
        margin: 0 0 10px 0;
        font-size: 1rem;
        color: #0f172a;
        font-weight: 800;
    }

    .reference-card p {
        margin: 0;
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.65;
    }

    .stat-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #0f766e, #0f5f75);
    }

    .stat-card .stat-label {
        color: #64748b;
        font-size: 0.86rem;
        margin-bottom: 10px;
        font-weight: 600;
    }

    .stat-card .stat-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.4px;
    }

    .remarks-box {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0f766e;
        padding: 16px 18px;
        border-radius: 12px;
        font-size: 0.96rem;
        color: #1e293b;
        line-height: 1.7;
        margin-top: 10px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .risk-pill {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 8px;
        letter-spacing: 0.1px;
    }

    .risk-normal {
        background: linear-gradient(180deg, #dcfce7 0%, #d1fae5 100%);
        color: #166534;
        border: 1px solid #86efac;
        box-shadow: 0 4px 10px rgba(34, 197, 94, 0.10);
    }

    .risk-moderate {
        background: linear-gradient(180deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 1px solid #facc15;
        box-shadow: 0 4px 10px rgba(234, 179, 8, 0.10);
    }

    .risk-high {
        background: linear-gradient(180deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border: 1px solid #fca5a5;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.10);
    }

    .divider-space {
        margin: 16px 0 8px 0;
    }

    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(226, 232, 240, 0.95);
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
    }

    .helper-note {
        color: #64748b;
        font-size: 0.88rem;
        margin-top: 8px;
        line-height: 1.55;
    }

    .record-meta {
        color: #64748b;
        font-size: 0.92rem;
        margin-top: 2px;
        margin-bottom: 16px;
    }

    .mini-note {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 2px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
        background: white;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stDateInput"] > div,
    div[data-testid="stTextInput"] > div,
    div[data-testid="stNumberInput"] > div {
        border-radius: 12px !important;
    }

    button[kind="primary"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(15, 118, 110, 0.18) !important;
    }

    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        color: #475569;
        font-size: 0.92rem;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def render_header(subtitle=""):
    st.markdown(f"""
        <div class="app-header">
            <div class="app-eyebrow">Healthcare AI</div>
            <h1>MIRA — Medical Intelligence Robotic Automation</h1>
            <p>{subtitle if subtitle else "Clinical health prediction and patient record management"}</p>
        </div>
    """, unsafe_allow_html=True)


def get_risk_level(glucose, haemoglobin, cholesterol):
    red_flags = 0
    caution_flags = 0

    if glucose >= 126:
        red_flags += 1
    elif glucose >= 100:
        caution_flags += 1

    if haemoglobin < 12:
        red_flags += 1
    elif haemoglobin < 13:
        caution_flags += 1

    if cholesterol >= 240:
        red_flags += 1
    elif cholesterol >= 200:
        caution_flags += 1

    if red_flags >= 1 and caution_flags >= 1:
        return "High Risk", "risk-high"
    if red_flags >= 2:
        return "High Risk", "risk-high"
    if red_flags == 1 or caution_flags >= 2:
        return "Moderate Risk", "risk-moderate"
    return "Normal", "risk-normal"


def render_risk_badge(glucose, haemoglobin, cholesterol):
    label, css_class = get_risk_level(glucose, haemoglobin, cholesterol)
    st.markdown(
        f"<div class='risk-pill {css_class}'>{label}</div>",
        unsafe_allow_html=True
    )


def render_reference_ranges():
    st.markdown("<div class='sub-heading'>Reference Ranges</div>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown("""
            <div class="reference-card">
                <h4>Glucose (mg/dL)</h4>
                <p>
                    Normal: 70–99<br>
                    Prediabetic: 100–125<br>
                    Diabetic risk: 126+
                </p>
            </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown("""
            <div class="reference-card">
                <h4>Haemoglobin (g/dL)</h4>
                <p>
                    Women: 12.0–15.5<br>
                    Men: 13.5–17.5<br>
                    Lower values may suggest anaemia
                </p>
            </div>
        """, unsafe_allow_html=True)

    with r3:
        st.markdown("""
            <div class="reference-card">
                <h4>Cholesterol (mg/dL)</h4>
                <p>
                    Desirable: below 200<br>
                    Borderline: 200–239<br>
                    High: 240+
                </p>
            </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.markdown("<div class='sidebar-title'>MIRA</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-subtitle'>Health Predictor</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    options=[
        "View All Patients",
        "Add New Patient",
        "Edit Patient",
        "Delete Patient"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### About")
st.sidebar.info(
    "Stores patient test values, generates AI-based health remarks, "
    "and supports quick screening through a visual risk indicator."
)


# --------------------------------------------------
# Page 1 - View All Patients
# --------------------------------------------------
if page == "View All Patients":
    render_header("Patient records overview and AI-generated health remarks")

    patients = get_all_patients()

    total_patients = len(patients)
    analysed_count = sum(1 for p in patients if p["remarks"] and len(p["remarks"]) > 10)
    pending_count = total_patients - analysed_count

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Patients</div>
                <div class="stat-value">{total_patients}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">AI Assessed</div>
                <div class="stat-value">{analysed_count}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Pending / Empty Remarks</div>
                <div class="stat-value">{pending_count}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider-space'></div>", unsafe_allow_html=True)

    if not patients:
        st.info("No patient records found. Add a patient to begin.")
    else:
        rows = []
        for p in patients:
            age = calculate_age(p["dob"]) if p["dob"] else "N/A"
            risk_label, _ = get_risk_level(p["glucose"], p["haemoglobin"], p["cholesterol"])

            rows.append({
                "ID": p["id"],
                "Full Name": p["full_name"],
                "Age": age,
                "Email": p["email"],
                "Glucose": p["glucose"],
                "Haemoglobin": p["haemoglobin"],
                "Cholesterol": p["cholesterol"],
                "Risk Indicator": risk_label,
                "Added On": p["created_at"].strftime("%d %b %Y") if p["created_at"] else "",
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<div class='mini-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)

        st.markdown("<div class='divider-space'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Patient Assessment Details</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Review the selected patient's screening badge and AI-generated interpretation.</div>", unsafe_allow_html=True)

        patient_names = {p["id"]: p["full_name"] for p in patients}
        selected_id = st.selectbox(
            "Select a patient",
            options=list(patient_names.keys()),
            format_func=lambda x: f"{x} — {patient_names[x]}"
        )

        if selected_id:
            selected = get_patient_by_id(selected_id)
            if selected:
                render_risk_badge(
                    selected["glucose"],
                    selected["haemoglobin"],
                    selected["cholesterol"]
                )
                st.markdown("<div class='helper-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='remarks-box'>{selected['remarks'] if selected['remarks'] else 'No AI remarks available yet.'}</div>",
                    unsafe_allow_html=True
                )


# --------------------------------------------------
# Page 2 - Add New Patient
# --------------------------------------------------
elif page == "Add New Patient":
    render_header("Create a new patient record and generate AI-based health remarks")

    st.markdown("""
        <div class="info-strip">
            Enter blood test values from the patient's lab report. The application will store the record
            and automatically generate an AI-based health assessment.
        </div>
    """, unsafe_allow_html=True)

    render_reference_ranges()

    with st.form("add_patient_form", clear_on_submit=True):
        st.markdown("<div class='sub-heading'>Patient Information</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g. Priya Sharma")
        with col2:
            email = st.text_input("Email Address *", placeholder="e.g. priya@example.com")

        dob = st.date_input(
            "Date of Birth *",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        st.markdown("<div class='sub-heading'>Blood Test Results</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            glucose = st.number_input(
                "Glucose (mg/dL) *",
                min_value=0.0,
                max_value=600.0,
                value=0.0,
                step=0.1,
                format="%.1f"
            )
        with c2:
            haemoglobin = st.number_input(
                "Haemoglobin (g/dL) *",
                min_value=0.0,
                max_value=25.0,
                value=0.0,
                step=0.1,
                format="%.1f"
            )
        with c3:
            cholesterol = st.number_input(
                "Cholesterol (mg/dL) *",
                min_value=0.0,
                max_value=1000.0,
                value=0.0,
                step=0.1,
                format="%.1f"
            )

        st.markdown("<div class='helper-note'>AI will generate a health assessment after saving the patient record.</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Save Patient & Generate AI Remarks", use_container_width=True)

    if submitted:
        errors = validate_all_fields(full_name, dob, email, glucose, haemoglobin, cholesterol)

        if errors:
            for err in errors:
                st.error(err)
        else:
            with st.spinner("Generating AI assessment..."):
                age = calculate_age(dob)
                remarks = get_health_remarks(full_name, age, glucose, haemoglobin, cholesterol)

            patient_id, db_error = add_patient(
                full_name=full_name.strip(),
                dob=dob,
                email=email.strip().lower(),
                glucose=glucose,
                haemoglobin=haemoglobin,
                cholesterol=cholesterol,
                remarks=remarks
            )

            if db_error:
                st.error(f"Could not save patient: {db_error}")
            else:
                st.success(f"Patient {full_name} added successfully! (ID: {patient_id})")
                render_risk_badge(glucose, haemoglobin, cholesterol)
                st.markdown("<div class='helper-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)
                st.markdown("### AI Health Prediction")
                st.markdown(f"<div class='remarks-box'>{remarks}</div>", unsafe_allow_html=True)


# --------------------------------------------------
# Page 3 - Edit Patient
# --------------------------------------------------
elif page == "Edit Patient":
    render_header("Update patient values and regenerate the AI assessment")

    patients = get_all_patients()

    if not patients:
        st.info("No patient records found. Add a patient first.")
    else:
        patient_options = {p["id"]: f"{p['full_name']} ({p['email']})" for p in patients}
        selected_id = st.selectbox(
            "Choose Patient to Edit",
            options=list(patient_options.keys()),
            format_func=lambda x: patient_options[x]
        )

        if selected_id:
            patient = get_patient_by_id(selected_id)

            if patient:
                added_on = patient["created_at"].strftime("%d %b %Y") if patient["created_at"] else "N/A"
                st.markdown(f"<div class='record-meta'>Editing record for <strong>{patient['full_name']}</strong> · Added on {added_on}</div>", unsafe_allow_html=True)

                render_reference_ranges()

                with st.form("edit_patient_form"):
                    st.markdown("<div class='sub-heading'>Patient Information</div>", unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        full_name = st.text_input("Full Name *", value=patient["full_name"])
                    with col2:
                        email = st.text_input("Email Address *", value=patient["email"])

                    dob = st.date_input(
                        "Date of Birth *",
                        value=patient["dob"],
                        min_value=date(1900, 1, 1),
                        max_value=date.today()
                    )

                    st.markdown("<div class='sub-heading'>Blood Test Results</div>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        glucose = st.number_input(
                            "Glucose (mg/dL) *",
                            min_value=0.0,
                            max_value=600.0,
                            value=float(patient["glucose"]),
                            step=0.1,
                            format="%.1f"
                        )
                    with c2:
                        haemoglobin = st.number_input(
                            "Haemoglobin (g/dL) *",
                            min_value=0.0,
                            max_value=25.0,
                            value=float(patient["haemoglobin"]),
                            step=0.1,
                            format="%.1f"
                        )
                    with c3:
                        cholesterol = st.number_input(
                            "Cholesterol (mg/dL) *",
                            min_value=0.0,
                            max_value=1000.0,
                            value=float(patient["cholesterol"]),
                            step=0.1,
                            format="%.1f"
                        )

                    st.markdown("<div class='sub-heading'>Current Assessment</div>", unsafe_allow_html=True)
                    render_risk_badge(
                        patient["glucose"],
                        patient["haemoglobin"],
                        patient["cholesterol"]
                    )

                    current_remarks = patient["remarks"] if patient["remarks"] else "No remarks generated yet."
                    st.markdown(f"<div class='remarks-box'>{current_remarks}</div>", unsafe_allow_html=True)
                    st.markdown("<div class='helper-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)
                    st.markdown("<div class='helper-note'>Saving will regenerate AI remarks using the updated values.</div>", unsafe_allow_html=True)

                    update_btn = st.form_submit_button(
                        "Update Record & Regenerate AI Remarks",
                        use_container_width=True
                    )

                if update_btn:
                    errors = validate_all_fields(full_name, dob, email, glucose, haemoglobin, cholesterol)

                    if not errors and email_exists_for_other(email.strip().lower(), selected_id):
                        errors.append("This email is already registered under another patient.")

                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        with st.spinner("Regenerating AI assessment..."):
                            age = calculate_age(dob)
                            new_remarks = get_health_remarks(full_name, age, glucose, haemoglobin, cholesterol)

                        success, err = update_patient(
                            patient_id=selected_id,
                            full_name=full_name.strip(),
                            dob=dob,
                            email=email.strip().lower(),
                            glucose=glucose,
                            haemoglobin=haemoglobin,
                            cholesterol=cholesterol,
                            remarks=new_remarks
                        )

                        if success:
                            st.success(f"Patient {full_name} updated successfully!")
                            render_risk_badge(glucose, haemoglobin, cholesterol)
                            st.markdown("<div class='helper-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)
                            st.markdown("### Updated AI Health Prediction")
                            st.markdown(f"<div class='remarks-box'>{new_remarks}</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"Update failed: {err}")


# --------------------------------------------------
# Page 4 - Delete Patient
# --------------------------------------------------
elif page == "Delete Patient":
    render_header("Delete patient records with confirmation")

    patients = get_all_patients()

    if not patients:
        st.info("No patient records found. Nothing to delete.")
    else:
        patient_options = {p["id"]: f"{p['full_name']} — {p['email']}" for p in patients}
        selected_id = st.selectbox(
            "Select Patient to Delete",
            options=list(patient_options.keys()),
            format_func=lambda x: patient_options[x]
        )

        if selected_id:
            patient = get_patient_by_id(selected_id)

            if patient:
                st.warning("This action permanently removes the selected patient record.")

                st.markdown("<div class='section-title'>Patient Details</div>", unsafe_allow_html=True)
                st.markdown("<div class='section-subtitle'>Review the selected record carefully before confirming deletion.</div>", unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"**Name:** {patient['full_name']}")
                    st.markdown(f"**Email:** {patient['email']}")
                    st.markdown(f"**Date of Birth:** {patient['dob']}")
                with d2:
                    st.markdown(f"**Glucose:** {patient['glucose']} mg/dL")
                    st.markdown(f"**Haemoglobin:** {patient['haemoglobin']} g/dL")
                    st.markdown(f"**Cholesterol:** {patient['cholesterol']} mg/dL")

                render_risk_badge(
                    patient["glucose"],
                    patient["haemoglobin"],
                    patient["cholesterol"]
                )

                st.markdown("<div class='helper-note'>Risk indicator is based on entered lab values and supports the AI-generated remarks.</div>", unsafe_allow_html=True)

                if patient["remarks"]:
                    st.markdown("### AI Remarks")
                    st.markdown(f"<div class='remarks-box'>{patient['remarks']}</div>", unsafe_allow_html=True)

                confirm = st.checkbox(
                    f"I confirm I want to permanently delete {patient['full_name']}'s record."
                )

                delete_btn = st.button(
                    "Delete Patient Record",
                    disabled=not confirm,
                    type="primary"
                )

                if delete_btn and confirm:
                    success, err = delete_patient(selected_id)
                    if success:
                        st.success(f"Patient {patient['full_name']} has been permanently deleted.")
                        st.rerun()
                    else:
                        st.error(f"Could not delete patient: {err}")