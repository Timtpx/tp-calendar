import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Transfer Pricing Fristen-Kalender", layout="wide")
st.title("🗓️ Transfer Pricing Fristen-Kalender für 2024")

fiscal_year_end = datetime(2024, 12, 31)

def calculate_due_date(code):
    if code == "6_months_after_fye":
        return fiscal_year_end + timedelta(days=182)
    elif code == "3_months_after_fye":
        return fiscal_year_end + timedelta(days=92)
    elif code == "5_months_after_fye":
        return fiscal_year_end + timedelta(days=153)
    elif code == "12_months_after_fye":
        return fiscal_year_end + timedelta(days=365)
    elif code == "6_months_after_local_file":
        return fiscal_year_end + timedelta(days=92 + 182)
    elif code == "with_tax_return":
        return "Mit Steuererklärung"
    elif code == "with_local_file":
        return "Mit Local File"
    elif code == "upon_request":
        return "Auf Anfrage"
    elif code == "available_at_tax_audit":
        return "Bereithalten zur Prüfung"
    elif code == "30_days_after_request":
        return "30 Tage nach Anfrage"
    else:
        return "Unbekannt"

# --- Upload Bereich ---
st.sidebar.header("📤 Länderliste hochladen")
uploaded_file = st.sidebar.file_uploader("CSV mit ISO-Ländercodes (z. B. DE, FR, CN)", type=["csv"])
view_mode = st.sidebar.radio("Ansicht wählen", ["Tabelle", "Zeitstrahl"])

# --- Fristendatenbank mit 34 Ländern ---
fristen_data = [
    {"code": "BE", "country": "Belgium", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "CH", "country": "Switzerland", "local_file": "available_at_tax_audit", "master_file": "upon_request"},
    {"code": "CZ", "country": "Czech Republic", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "FR", "country": "France", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "IT", "country": "Italy", "local_file": "available_at_tax_audit", "master_file": "30_days_after_request"},
    {"code": "NL", "country": "Netherlands", "local_file": "6_months_after_fye", "master_file": "6_months_after_local_file"},
    {"code": "PL", "country": "Poland", "local_file": "3_months_after_fye", "master_file": "upon_request"},
    {"code": "SE", "country": "Sweden", "local_file": "6_months_after_fye", "master_file": "upon_request"},
    {"code": "SK", "country": "Slovakia", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "ES", "country": "Spain", "local_file": "with_tax_return", "master_file": "6_months_after_fye"},
    {"code": "GB", "country": "United Kingdom", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "HU", "country": "Hungary", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "RU", "country": "Russia", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "TR", "country": "Türkiye", "local_file": "with_tax_return", "master_file": "upon_request"},
    {"code": "US", "country": "United States", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "CA", "country": "Canada", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "MX", "country": "Mexico", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "CL", "country": "Chile", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "AR", "country": "Argentina", "local_file": "5_months_after_fye", "master_file": "12_months_after_fye"},
    {"code": "CO", "country": "Colombia", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "SG", "country": "Singapore", "local_file": "with_tax_return", "master_file": "upon_request"},
    {"code": "TH", "country": "Thailand", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "JP", "country": "Japan", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "KR", "country": "South Korea", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "CN", "country": "China", "local_file": "6_months_after_fye", "master_file": "with_local_file"},
    {"code": "MY", "country": "Malaysia", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "TW", "country": "Taiwan", "local_file": "with_tax_return", "master_file": "with_local_file"},
    {"code": "FI", "country": "Finland", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "BR", "country": "Brazil", "local_file": "with_tax_return", "master_file": "upon_request"},
    {"code": "AU", "country": "Australia", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "NZ", "country": "New Zealand", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "ZA", "country": "South Africa", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "AE", "country": "United Arab Emirates", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
]

# --- Verarbeitung & Anzeige ---
if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)
    selected_codes = df_upload.iloc[:, 0].str.strip().tolist()

    rows = []
    timeline_events = []

    for entry in fristen_data:
        if entry["code"] in selected_codes:
            local_due = calculate_due_date(entry["local_file"])
            master_due = calculate_due_date(entry["master_file"])
            rows.append({"Land": entry["country"], "Local File fällig": local_due, "Master File fällig": master_due})

            if isinstance(local_due, datetime):
                timeline_events.append({
                    "start_date": {"year": local_due.year, "month": local_due.month, "day": local_due.day},
                    "text": {"headline": f"{entry['country']}: Local File"}
                })
            if isinstance(master_due, datetime):
                timeline_events.append({
                    "start_date": {"year": master_due.year, "month": master_due.month, "day": master_due.day},
                    "text": {"headline": f"{entry['country']}: Master File"}
                })

    if rows:
        if view_mode == "Tabelle":
            df_result = pd.DataFrame(rows)
            st.success("✅ Fristen erfolgreich ermittelt:")
            st.dataframe(df_result, use_container_width=True)
        else:
            st.subheader("🕒 Zeitstrahl der Fristen")
            timeline_data = {"events": timeline_events}
            components.html(
                f"""
                <iframe srcdoc='{json.dumps(timeline_data)}'
                        width='100%' height='600' frameborder='0'></iframe>
                """,
                height=600
            )
    else:
        st.warning("Keine passenden Länder in der Datenbank gefunden.")
else:
    st.info("Bitte lade eine Länderliste als CSV hoch, um die Fristen zu sehen.")

st.markdown("""
#### 📥 Nächste Schritte
- Export als Excel oder ICS-Datei (Kalenderformat)
- Erweiterung um CbCR und andere Dokumentationspflichten
""")
