import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from sidebar import render_sidebar

st.set_page_config(page_title="PIZZA TIFOSI - Charges Fixes", page_icon="🧾", layout="wide")
render_sidebar()

conn = st.connection("gsheets", type="gsheets")

@st.cache_data(ttl=1)
def load_charges():
    try:
        return conn.read(worksheet="Charges_Fixes", ttl=0)
    except:
        return pd.DataFrame()

df_charges = load_charges()

with st.expander("➕ Ajouter une Charge Fixe (Sincronización Directa)", expanded=False):
    with st.form("form_nueva_charge"):
        col1, col2 = st.columns(2)
        with col1:
            mois_input = st.date_input("Mois", value=datetime.now())
            cat = st.selectbox("Catégorie de Charge", ["Loyer", "Électricité", "Eau"])
            montant = st.number_input("Montant (€)", min_value=0.0, step=10.0)
        with col2:
            pago_input = st.date_input("Date de Paiement (opcional)", value=datetime.now())
            statut = st.selectbox("Statut", ["Payé", "En att..."])
            
        submit_btn = st.form_submit_button("💾 Sauvegarder dans Google Sheets")
        
        if submit_btn:
            mois_str = mois_input.strftime("%d/%m/%Y")
            pago_str = pago_input.strftime("%d/%m/%Y") if statut == "Payé" else "-"
            
            nueva_fila = pd.DataFrame([{
                "Mois": mois_str,
                "Catégorie de Charge": cat,
                "Montant": montant,
                "Date de Paiement": pago_str,
                "Statut": statut
            }])
            try:
                updated_df = pd.concat([df_charges, nueva_fila], ignore_index=True)
                conn.update(worksheet="Charges_Fixes", data=updated_df)
                st.success("¡Carga fija guardada en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

filas_html = ""
if not df_charges.empty:
    for _, row in df_charges.iterrows():
        mois = str(row.get("Mois", ""))
        cat = str(row.get("Catégorie de Charge", "Loyer"))
        montant = float(row.get("Montant", 0) or 0)
        pago = str(row.get("Date de Paiement", ""))
        statut = str(row.get("Statut", "Payé"))
        
        badge_cat = "badge-loyer" if cat.strip() == "Loyer" else ("badge-electricite" if cat.strip() == "Électricité" else "badge-eau")
        badge_stat = "badge-paye" if statut.strip() == "Payé" else "badge-attente"
        
        filas_html += f"""
            <tr>
              <td>{mois}</td>
              <td><span class="{badge_cat}">{cat}</span></td>
              <td class="fw-bold text-danger">{montant:,.0f} €</td>
              <td>{pago if pago and pago != 'nan' else '-'}</td>
              <td><span class="{badge_stat}">{statut}</span></td>
            </tr>
        """

html_charges = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem; }}
    .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; }}
    .badge-loyer {{ background-color: #e0f2fe; color: #0369a1; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
    .badge-electricite {{ background-color: #fef3c7; color: #d97706; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
    .badge-eau {{ background-color: #f3e8ff; color: #7e22ce; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
    .badge-paye {{ background-color: #dcfce7; color: #15803d; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; }}
    .badge-attente {{ background-color: #fee2e2; color: #b91c1c; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; }}
  </style>
</head>
<body>
  <div class="table-card">
    <h6 class="fw-bold mb-3">Registre des Charges Fixes (Google Sheets)</h6>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0 small">
        <thead class="table-light">
          <tr><th>Mois</th><th>Catégorie de Charge</th><th>Montant</th><th>Date de Paiement</th><th>Statut</th></tr>
        </thead>
        <tbody>{filas_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
components.html(html_charges, height=800, scrolling=False)