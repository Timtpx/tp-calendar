import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Transfer Pricing Fristen-Kalender", layout="wide")
st.title("🗓️ Transfer Pricing Fristen-Kalender für 2024")

# Geschäftsjahr
fiscal_year_end = datetime(2024, 12, 31)

def calculate_due_date(code):
    if code == "6_months_after_fye":
        return fiscal_year_end + timedelta(days=182)
    elif code == "3_months_after_fye":
        return fiscal_year_end + timedelta(days=92)
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

# Hochladen der Länderliste
st.sidebar.header("📤 Länderliste hochladen")
uploaded_file = st.sidebar.file_uploader("CSV mit ISO-Ländercodes (z. B. DE, FR, CN)", type=["csv"])

# Fristendatenbank (vereinfachte Demo-Daten)
fristen_data = [
    {"code": "FR", "country": "France", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "DE", "country": "Germany", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "IT", "country": "Italy", "local_file": "available_at_tax_audit", "master_file": "30_days_after_request"},
    {"code": "CN", "country": "China", "local_file": "6_months_after_fye", "master_file": "with_local_file"},
    {"code": "MX", "country": "Mexico", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "US", "country": "United States", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "GB", "country": "United Kingdom", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "PL", "country": "Poland", "local_file": "3_months_after_fye", "master_file": "upon_request"},
    {"code": "SE", "country": "Sweden", "local_file": "6_months_after_fye", "master_file": "upon_request"},
    {"code": "JP", "country": "Japan", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "TH", "country": "Thailand", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "AU", "country": "Australia", "local_file": "with_tax_return", "master_file": "6_months_after_local_file"},
    {"code": "NL", "country": "Netherlands", "local_file": "6_months_after_fye", "master_file": "6_months_after_local_file"},
    {"code": "CA", "country": "Canada", "local_file": "upon_request", "master_file": "upon_request"},
    {"code": "CH", "country": "Switzerland", "local_file": "available_at_tax_audit", "master_file": "upon_request"},
    {"code": "KR", "country": "South Korea", "local_file": "3_months_after_fye", "master_file": "3_months_after_fye"},
    {"code": "BR", "country": "Brazil", "local_file": "with_tax_return", "master_file": "upon_request"},
    {"code": "AR", "country": "Argentina", "local_file": "5_months_after_fye", "master_file": "12_months_after_fye"},
]

# Daten extrahieren und anzeigen
if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)
    selected_codes = df_upload.iloc[:, 0].str.strip().tolist()

    rows = []
    for entry in fristen_data:
        if entry["code"] in selected_codes:
            rows.append({
                "Land": entry["country"],
                "Local File fällig": calculate_due_date(entry["local_file"]),
                "Master File fällig": calculate_due_date(entry["master_file"])
            })

    if rows:
        df_result = pd.DataFrame(rows)
        st.success("✅ Fristen erfolgreich ermittelt:")
        st.dataframe(df_result, use_container_width=True)
    else:
        st.warning("Keine passenden Länder in der Datenbank gefunden.")
else:
    st.info("Bitte lade eine Länderliste als CSV hoch, um die Fristen zu sehen.")

st.markdown("""#### 📥 Nächste Schritte
- Erweiterung der Fristendatenbank auf alle Länder
- Export als Excel oder ICS-Datei (Kalenderformat)
- Visualisierung per Timeline
""")
