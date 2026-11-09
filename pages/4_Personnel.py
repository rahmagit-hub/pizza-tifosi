import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from sidebar import render_sidebar

st.set_page_config(page_title="PIZZA TIFOSI - Personnel & Paie", page_icon="👥", layout="wide")
render_sidebar()

conn = st.connection("gsheets", type="gsheets")

@st.cache_data(ttl=1)
def load_personnel():
    try:
        return conn.read(worksheet="Personnel_Associés", ttl=0)
    except:
        return pd.DataFrame()

df_personnel = load_personnel()

with st.expander("➕ Ajouter un Paiement Personnel (Sincronización Directa)", expanded=False):
    with st.form("form_nuevo_employe"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.selectbox("Employé", ["Hacene", "Karim", "Amel", "Wael", "Yacer"])
            periode = st.selectbox("Période", ["Mois", "Quinzaine"])
            fecha_input = st.date_input("Date Paiement", value=datetime.now())
        with col2:
            salaire = st.number_input("Salaire Base (€)", min_value=0.0, step=50.0)
            extra = st.number_input("Heures Extra (€)", min_value=0.0, step=10.0)
            metodo = st.selectbox("Méthode Paiement", ["Virement", "Espèces"])
            
        submit_btn = st.form_submit_button("💾 Sauvegarder dans Google Sheets")
        
        if submit_btn:
            fecha_str = fecha_input.strftime("%d/%m/%Y")
            total = salaire + extra
            nueva_fila = pd.DataFrame([{
                "Nom": nom,
                "Période": periode,
                "Date Paiement": fecha_str,
                "Salaire Base": salaire,
                "Heures Extra": extra,
                "Total Payé": total,
                "Méthode Paiement": metodo
            }])
            try:
                updated_df = pd.concat([df_personnel, nueva_fila], ignore_index=True)
                conn.update(worksheet="Personnel_Associés", data=updated_df)
                st.success("¡Pago guardado en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

filas_html = ""
if not df_personnel.empty:
    for _, row in df_personnel.iterrows():
        nom = str(row.get("Nom", ""))
        periode = str(row.get("Période", "Mois"))
        date_pago = str(row.get("Date Paiement", ""))
        salaire = float(row.get("Salaire Base", 0) or 0)
        extra = float(row.get("Heures Extra", 0) or 0)
        total = float(row.get("Total Payé", 0) or (salaire + extra))
        metodo = str(row.get("Méthode Paiement", "Virement"))
        badge_class = "badge-virement" if metodo.strip() == "Virement" else "badge-especes"
        
        filas_html += f"""
            <tr>
              <td class="fw-bold">{nom}</td>
              <td>{periode}</td>
              <td>{date_pago}</td>
              <td>{salaire:,.0f} €</td>
              <td>{f"{extra:,.0f} €" if extra > 0 else "-"}</td>
              <td class="fw-bold text-success">{total:,.0f} €</td>
              <td><span class="{badge_class}">{metodo}</span></td>
            </tr>
        """

html_personnel = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem; }}
    .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; }}
    .badge-virement {{ background-color: #f3e8ff; color: #7e22ce; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
    .badge-especes {{ background-color: #e0f2fe; color: #0369a1; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
  </style>
</head>
<body>
  <div class="table-card">
    <h6 class="fw-bold mb-3">Registre des Paiements & Salaires (Google Sheets)</h6>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0 small">
        <thead class="table-light">
          <tr><th>Nom</th><th>Période</th><th>Date Paiement</th><th>Salaire Base</th><th>Heures Extra</th><th>Total Payé</th><th>Méthode Paiement</th></tr>
        </thead>
        <tbody>{filas_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
components.html(html_personnel, height=800, scrolling=False)