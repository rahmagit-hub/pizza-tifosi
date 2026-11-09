import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from sidebar import render_sidebar

st.set_page_config(page_title="PIZZA TIFOSI - Inventaire & Stocks", page_icon="📦", layout="wide")
render_sidebar()

conn = st.connection("gsheets", type="gsheets")

@st.cache_data(ttl=1)
def load_inventaire():
    try:
        return conn.read(worksheet="Contrôle Inventaire", ttl=0)
    except:
        return pd.DataFrame()

df_inventaire = load_inventaire()

# FORMULARIO DE REGISTRO DIRECTO A GOOGLE SHEETS
with st.expander("➕ Ajouter un Article au Stock (Sincronización Directa)", expanded=False):
    with st.form("form_nuevo_article"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom du Produit", placeholder="Ex: Mozzarella, Coca...")
            cat = st.selectbox("Catégorie", ["Fromage", "Viande", "Boisson"])
        with col2:
            stock = st.number_input("Stock Actuel", min_value=0.0, step=1.0)
            unite = st.selectbox("Unité", ["Boite", "Kg", "Unité"])
            
        exp_input = st.date_input("Date d'expiration", value=datetime.now())
        
        submit_btn = st.form_submit_button("💾 Sauvegarder dans Google Sheets")
        
        if submit_btn:
            exp_str = exp_input.strftime("%d/%m/%Y")
            nueva_fila = pd.DataFrame([{
                "Nom du Produit": nom,
                "Catégorie": cat,
                "Stock Actuel": stock,
                "Unité": unite,
                "Date d'expiration": exp_str,
                "Jours Restants": "",
                "Expiration Proche": "OK"
            }])
            try:
                updated_df = pd.concat([df_inventaire, nueva_fila], ignore_index=True)
                conn.update(worksheet="Contrôle Inventaire", data=updated_df)
                st.success("¡Artículo guardado en Google Sheets!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

# TABLA VISUAL
filas_html = ""
fecha_actual = datetime(2026, 11, 7)
if not df_inventaire.empty:
    for _, row in df_inventaire.iterrows():
        nom = str(row.get("Nom du Produit", ""))
        cat = str(row.get("Catégorie", "Fromage"))
        stock = row.get("Stock Actuel", 0)
        unite = str(row.get("Unité", "Boite"))
        exp = str(row.get("Date d'expiration", ""))
        
        try:
            exp_date = pd.to_datetime(exp, format='%d/%m/%Y', errors='coerce')
            if pd.isna(exp_date):
                exp_date = pd.to_datetime(exp, errors='coerce')
            dias = (exp_date - pd.Timestamp(fecha_actual)).days if pd.notna(exp_date) else 0
        except:
            dias = 0

        cat_class = "cat-fromage" if cat.strip() == "Fromage" else ("cat-viande" if cat.strip() == "Viande" else "cat-boisson")
        alert_html = '<span class="alert-proche">🚨 PROCHE EXPIRATION</span>' if dias <= 5 else '<span class="alert-ok">OK</span>'
        
        filas_html += f"""
            <tr>
              <td class="fw-bold">{nom}</td>
              <td><span class="cat-badge {cat_class}">{cat}</span></td>
              <td class="fw-bold">{stock}</td>
              <td>{unite}</td>
              <td>{exp}</td>
              <td class="text-center fw-bold {'text-danger' if dias <= 5 else ''}">{dias}</td>
              <td>{alert_html}</td>
            </tr>
        """

html_inventaire = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 1rem; }}
    .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; }}
    .cat-badge {{ font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }}
    .cat-fromage {{ background-color: #f3e8ff; color: #7e22ce; }}
    .cat-viande {{ background-color: #e0f2fe; color: #0369a1; }}
    .cat-boisson {{ background-color: #ffedd5; color: #c2410c; }}
    .alert-ok {{ background-color: #dcfce7; color: #15803d; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; }}
    .alert-proche {{ background-color: #fee2e2; color: #b91c1c; font-weight: 800; font-size: 0.75rem; padding: 0.4rem 0.8rem; border-radius: 20px; }}
  </style>
</head>
<body>
  <div class="table-card">
    <h6 class="fw-bold mb-3">État des Stocks & Péremptions (Google Sheets)</h6>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0 small">
        <thead class="table-light">
          <tr><th>Nom du Produit</th><th>Catégorie</th><th>Stock Actuel</th><th>Unité</th><th>Date d'expiration</th><th class="text-center">Jours Restants</th><th>Expiration Proche</th></tr>
        </thead>
        <tbody>{filas_html}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
components.html(html_inventaire, height=800, scrolling=False)