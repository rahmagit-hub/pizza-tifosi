import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from sidebar import render_sidebar

st.set_page_config(page_title="PIZZA TIFOSI - Achats", page_icon="🛍️", layout="wide")
render_sidebar()

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=1)
def load_achats():
    try:
        return conn.read(worksheet="Achats-Depences", ttl=0)
    except:
        return pd.DataFrame()

df_achats = load_achats()

with st.expander("➕ Enregistrer un Nouvel Achat", expanded=False):
    with st.form("form_nuevo_achat"):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_input = st.date_input("Date d'achat", value=datetime.now())
            producto = st.text_input("Produit", placeholder="Ex: Mozzarella")
        with col2:
            provenance = st.selectbox("Provenance", ["Cotsco", "Fournisseur"])
            quantite = st.text_input("Quantité", placeholder="Ex: 10 kg")
        with col3:
            precio = st.number_input("Prix Total (€)", min_value=0.0, step=10.0)
            
        submit_btn = st.form_submit_button("💾 Sauvegarder dans Google Sheets")
        
        if submit_btn:
            fecha_str = fecha_input.strftime("%d/%m/%Y")
            nueva_fila = pd.DataFrame([{
                "Date d'achat": fecha_str,
                "Produit": producto,
                "Quantité": quantite,
                "Prix Total": precio,
                "Provenance": provenance,
                "Photo Ticket": ""
            }])
            try:
                updated_df = pd.concat([df_achats, nueva_fila], ignore_index=True)
                conn.update(worksheet="Achats-Depences", data=updated_df)
                st.success("¡Compra guardada en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

filas_html = ""
if not df_achats.empty:
    for _, row in df_achats.iterrows():
        date_val = str(row.get("Date d'achat", ""))
        prod = str(row.get("Produit", ""))
        cant = str(row.get("Quantité", ""))
        precio = float(row.get("Prix Total", 0) or 0)
        prov = str(row.get("Provenance", "Cotsco"))
        prov_class = "prov-cotsco" if prov.strip() == "Cotsco" else "prov-fournisseur"
        
        filas_html += f"""
            <tr>
              <td class="fw-bold">{date_val}</td>
              <td><span class="prov-badge {prov_class}">{prov}</span></td>
              <td class="fw-bold">{prod} ({cant})</td>
              <td class="fw-bold text-primary">{precio:,.2f} €</td>
            </tr>
        """

html_achats = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem; }}
    .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; }}
    .prov-badge {{ font-weight: 600; font-size: 0.8rem; padding: 0.3rem 0.8rem; border-radius: 20px; }}
    .prov-cotsco {{ background-color: #e0f2fe; color: #0369a1; }}
    .prov-fournisseur {{ background-color: #fae8ff; color: #86198f; }}
  </style>
</head>
<body>
  <div class="table-card">
    <h6 class="fw-bold mb-3">Journal des Achats (Google Sheets)</h6>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0 small">
        <thead class="table-light">
          <tr><th>Date d'achat</th><th>Provenance</th><th>Produit & Quantité</th><th>Prix Total</th></tr>
        </thead>
        <tbody>{filas_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
components.html(html_achats, height=800, scrolling=False)