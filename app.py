import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from sidebar import render_sidebar
from google.oauth2 import service_account

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
cfg = dict(st.secrets["connections"]["gsheets"])
st.write(sorted(cfg.keys()))
st.write(len(cfg.get("private_key", "")), cfg.get("private_key", "")[:40], repr(cfg.get("private_key", "")[-30:]))
creds = service_account.Credentials.from_service_account_info(cfg)
st.success("Credenciales OK")

conn = st.connection("gsheets", type="gsheets")
@st.cache_data(ttl=1)
def load_all_dashboard_data():
    try:
        df_v = conn.read(worksheet="Ventes-Caisse", ttl=0)
    except Exception:
        df_v = pd.DataFrame()
    try:
        df_a = conn.read(worksheet="Achats-Depences", ttl=0)
    except Exception:
        df_a = pd.DataFrame()
    try:
        df_i = conn.read(worksheet="Contrôle Inventaire", ttl=0)
    except Exception:
        df_i = pd.DataFrame()
    return df_v, df_a, df_i

df_ventas, df_achats, df_inv = load_all_dashboard_data()

total_ventas = df_ventas["Total Ventes"].sum() if not df_ventas.empty and "Total Ventes" in df_ventas.columns else 0.0
redevance = df_ventas["Redevance Franchise 3%"].sum() if not df_ventas.empty and "Redevance Franchise 3%" in df_ventas.columns else total_ventas * 0.03
total_achats = df_achats["Prix Total"].sum() if not df_achats.empty and "Prix Total" in df_achats.columns else 0.0

# Alertes péremption
alertas_count = 0
filas_alertas = ""
fecha_actual = datetime(2026, 11, 7)

if not df_inv.empty:
    for _, row in df_inv.iterrows():
        nom = str(row.get("Nom du Produit", ""))
        stock = row.get("Stock Actuel", 0)
        unite = str(row.get("Unité", ""))
        exp = str(row.get("Date d'expiration", ""))
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