import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from sidebar import render_sidebar

st.set_page_config(page_title="PIZZA TIFOSI - Ventes / Caisse", page_icon="🛒", layout="wide")
render_sidebar()

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=1)
def load_ventas():
    try:
        return conn.read(worksheet="Ventes-Caisse", ttl=0)
    except:
        return pd.DataFrame()

df_ventas = load_ventas()

with st.expander("➕ Enregistrer une Nouvelle Journée de Vente", expanded=False):
    with st.form("form_nueva_venta"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            fecha_input = st.date_input("Date", value=datetime.now())
        with col2:
            especes = st.number_input("Espèces (€)", min_value=0.0, step=10.0)
        with col3:
            carte = st.number_input("Carte Bancaire (€)", min_value=0.0, step=10.0)
        with col4:
            livraison = st.number_input("Livraison (€)", min_value=0.0, step=10.0)
            
        statut_res = st.selectbox("Statut Réserve", ["Non", "Oui"])
        submit_btn = st.form_submit_button("💾 Sauvegarder dans Google Sheets")
        
        if submit_btn:
            total_v = especes + carte + livraison
            redevance_v = total_v * 0.03
            fecha_str = fecha_input.strftime("%d/%m/%Y")
            
            nueva_fila = pd.DataFrame([{
                "Date": fecha_str,
                "Espèces": especes,
                "Carte Bancaire": carte,
                "Livraison": livraison,
                "Total Ventes": total_v,
                "Redevance Franchise 3%": redevance_v,
                "Statut Réserve": statut_res
            }])
            
            try:
                updated_df = pd.concat([df_ventas, nueva_fila], ignore_index=True)
                conn.update(worksheet="Ventes-Caisse", data=updated_df)
                st.success("¡Venta guardada y sincronizada en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

filas_html = ""
if not df_ventas.empty:
    for _, row in df_ventas.iterrows():
        date_val = str(row.get('Date', ''))
        esp = float(row.get('Espèces', 0) or 0)
        cb = float(row.get('Carte Bancaire', 0) or 0)
        liv = float(row.get('Livraison', 0) or 0)
        total = float(row.get('Total Ventes', 0) or (esp + cb + liv))
        redevance = float(row.get('Redevance Franchise 3%', 0) or (total * 0.03))
        statut = str(row.get('Statut Réserve', 'Non'))
        status_class = "status-oui" if statut.strip() == "Oui" else "status-non"
        
        filas_html += f"""
            <tr>
              <td class="fw-bold">{date_val}</td>
              <td>{esp:,.2f} €</td>
              <td>{cb:,.2f} €</td>
              <td>{liv:,.2f} €</td>
              <td class="fw-bold text-primary">{total:,.2f} €</td>
              <td class="fw-bold text-danger">{redevance:,.2f} €</td>
              <td class="text-center"><span class="status-select {status_class}">{statut}</span></td>
            </tr>
        """

html_ventas = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem; }}
    .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; }}
    .status-select {{ border-radius: 20px; font-weight: 700; font-size: 0.8rem; padding: 0.3rem 0.8rem; }}
    .status-oui {{ background-color: #dcfce7; color: #15803d; }}
    .status-non {{ background-color: #fee2e2; color: #b91c1c; }}
  </style>
</head>
<body>
  <div class="table-card">
    <h6 class="fw-bold mb-3">Journal des Ventes (Google Sheets)</h6>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0 small">
        <thead class="table-light">
          <tr><th>Date</th><th>Espèces</th><th>Carte Bancaire</th><th>Livraison</th><th class="text-primary">Total Ventes</th><th class="text-danger">Redevance (3%)</th><th class="text-center">Statut Réserve</th></tr>
        </thead>
        <tbody>{filas_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
components.html(html_ventas, height=800, scrolling=False)