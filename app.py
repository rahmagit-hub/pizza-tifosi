import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Tableau de Bord",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .block-container { padding: 1rem 0rem 0rem 0rem !important; max-width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# Inicializar conexión con st-gsheets-connection
conn = st.connection("gsheets", type="gsheets")

@st.cache_data(ttl=1)
def load_all_dashboard_data():
    def fetch_sheet(sheet_name):
        try:
            df = conn.read(worksheet=sheet_name, ttl=0)
            if df is not None and not df.empty:
                df.columns = df.columns.astype(str).str.strip()
                return df
        except Exception as e:
            st.warning(f"⚠️ Atención al cargar '{sheet_name}': {e}")
        return pd.DataFrame()

    df_v = fetch_sheet("Ventes-Caisse")
    df_a = fetch_sheet("Achats-Depences")
    df_i = fetch_sheet("Contrôle Inventaire")
    
    return df_v, df_a, df_i

df_ventas, df_achats, df_inv = load_all_dashboard_data()

# Conversión y procesamiento seguro de Ventas
if not df_ventas.empty and "Total Ventes" in df_ventas.columns:
    total_ventas_series = pd.to_numeric(
        df_ventas["Total Ventes"].astype(str).str.replace('€', '').str.replace(' ', '').str.replace(',', '.'), 
        errors='coerce'
    )
    total_ventas = total_ventas_series.sum()
else:
    total_ventas = 0.0

if not df_ventas.empty and "Redevance Franchise 3%" in df_ventas.columns:
    redevance_series = pd.to_numeric(
        df_ventas["Redevance Franchise 3%"].astype(str).str.replace('€', '').str.replace(' ', '').str.replace(',', '.'), 
        errors='coerce'
    )
    redevance = redevance_series.sum()
else:
    redevance = total_ventas * 0.03

# Conversión y procesamiento seguro de Compras
if not df_achats.empty and "Prix Total" in df_achats.columns:
    achats_series = pd.to_numeric(
        df_achats["Prix Total"].astype(str).str.replace('€', '').str.replace(' ', '').str.replace(',', '.'), 
        errors='coerce'
    )
    total_achats = achats_series.sum()
else:
    total_achats = 0.0

# Alertas de caducidad
alertas_count = 0
filas_alertas = ""
fecha_actual = datetime(2026, 11, 7)

if not df_inv.empty:
    for _, row in df_inv.iterrows():
        nom = str(row.get("Nom du Produit", "")).strip()
        stock = row.get("Stock Actuel", 0)
        unite = str(row.get("Unité", "")).strip()
        exp = str(row.get("Date d'expiration", "")).strip()
        
        try:
            exp_date = pd.to_datetime(exp, format='%d/%m/%Y', errors='coerce')
            if pd.isna(exp_date):
                exp_date = pd.to_datetime(exp, errors='coerce')
            dias = (exp_date - pd.Timestamp(fecha_actual)).days if pd.notna(exp_date) else 99
        except Exception:
            dias = 99
            
        if dias <= 5:
            alertas_count += 1
            badge = f'<span class="badge bg-danger">🔴 Urgent ({dias} jours)</span>' if dias >= 0 else '<span class="badge bg-danger">🔴 Expiré</span>'
            filas_alertas += f'<tr><td class="fw-bold">{nom}</td><td>{stock} {unite}</td><td>{exp}</td><td>{badge}</td></tr>'

html_dashboard = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1e293b; margin: 0; padding: 0; }}
    .main-content {{ padding: 2rem; }}
    .header-card, .stat-card, .table-card {{ background: #ffffff; border-radius: 12px; padding: 1.25rem; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem; }}
    .stat-value {{ font-size: 1.8rem; font-weight: 700; color: #0f172a; }}
    .stat-label {{ font-size: 0.875rem; color: #64748b; }}
  </style>
</head>
<body>
  <div class="main-content">
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-bar-chart-fill text-warning me-2"></i>Tableau de Bord</h3>
        <p class="text-muted m-0 small mt-1">Données en temps réel synchronisées avec Google Sheets</p>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Ventes Totales</div><div class="stat-value">{total_ventas:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Redevance Franchise (3%)</div><div class="stat-value text-danger">{redevance:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Achats Totaux</div><div class="stat-value">{total_achats:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Alertes Péremption</div><div class="stat-value text-warning">{alertas_count} produits</div></div></div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-exclamation-triangle-fill me-2 text-danger"></i>Alertes de Péremption (Prochains à caducar)</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
          <thead class="table-light">
            <tr><th>Produit</th><th>Quantité</th><th>Date de Péremption</th><th>Statut</th></tr>
          </thead>
          <tbody>
            {filas_alertas if filas_alertas else '<tr><td colspan="4" class="text-center text-muted">Aucun produit en alerte</td></tr>'}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</html>
"""

components.html(html_dashboard, height=800, scrolling=False)