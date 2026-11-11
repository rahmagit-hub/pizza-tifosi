import html
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
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

conn = st.connection("gsheets", type=GSheetsConnection)


# ---------- Helpers ----------
def parse_num(v):
    """Convierte '1.234,56 €', '12,5', 12.5, NaN... en float."""
    if pd.isna(v):
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("€", "").replace("\xa0", "").replace(" ", "").strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def col_sum(df, col):
    """Suma de una columna (None si no existe)."""
    if df.empty or col not in df.columns:
        return None
    return df[col].map(parse_num).sum()


def txt(v):
    """Texto seguro para HTML ('' si está vacío)."""
    return "" if pd.isna(v) else html.escape(str(v))


# ---------- Carga de datos ----------
@st.cache_data(ttl=60)
def load_all_dashboard_data():
    errores = []
    hojas = {}
    for clave, nombre in [
        ("ventes", "Ventes-Caisse"),
        ("achats", "Achats-Depences"),
        ("inv", "Contrôle Inventaire"),
    ]:
        try:
            hojas[clave] = conn.read(worksheet=nombre, ttl=0).dropna(how="all")
        except Exception as e:
            hojas[clave] = pd.DataFrame()
            errores.append(f"No se pudo leer la hoja «{nombre}»: {e}")
    return hojas["ventes"], hojas["achats"], hojas["inv"], errores


df_ventas, df_achats, df_inv, errores = load_all_dashboard_data()

for err in errores:
    st.warning(err)

# ---------- Cálculos ----------
total_ventas = col_sum(df_ventas, "Total Ventes") or 0.0
redevance = col_sum(df_ventas, "Redevance Franchise 3%")
if redevance is None:
    redevance = total_ventas * 0.03
total_achats = col_sum(df_achats, "Prix Total") or 0.0

# Fecha real de hoy (antes estaba fija en 07/11/2026)
hoy = pd.Timestamp.now(tz="Europe/Madrid").tz_localize(None).normalize()

alertas = []
if not df_inv.empty:
    for _, row in df_inv.iterrows():
        exp_date = pd.to_datetime(row.get("Date d'expiration"), dayfirst=True, errors="coerce")
        if pd.isna(exp_date):
            continue
        dias = (exp_date.normalize() - hoy).days
        if dias <= 5:
            alertas.append((dias, row, exp_date))

alertas.sort(key=lambda x: x[0])
alertas_count = len(alertas)

filas_alertas = ""
for dias, row, exp_date in alertas:
    nom = txt(row.get("Nom du Produit"))
    stock = txt(row.get("Stock Actuel"))
    unite = txt(row.get("Unité"))
    if dias < 0:
        badge = '<span class="badge bg-danger">🔴 Expiré</span>'
    else:
        badge = f'<span class="badge bg-danger">🔴 Urgent ({dias} jours)</span>'
    filas_alertas += (
        f'<tr><td class="fw-bold">{nom}</td><td>{stock} {unite}</td>'
        f'<td>{exp_date.strftime("%d/%m/%Y")}</td><td>{badge}</td></tr>'
    )

sin_alertas = '<tr><td colspan="4" class="text-center text-muted">Aucun produit en alerte</td></tr>'

# ---------- HTML ----------
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
        <p class="text-muted m-0 small mt-1">Données synchronisées avec Google Sheets (mise à jour chaque minute)</p>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Ventes Totales</div><div class="stat-value">{total_ventas:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Redevance Franchise (3%)</div><div class="stat-value text-danger">{redevance:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Achats Totaux</div><div class="stat-value">{total_achats:,.2f} €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Alertes Péremption</div><div class="stat-value text-warning">{alertas_count} produits</div></div></div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-exclamation-triangle-fill me-2 text-danger"></i>Alertes de Péremption</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
          <thead class="table-light">
            <tr><th>Produit</th><th>Quantité</th><th>Date de Péremption</th><th>Statut</th></tr>
          </thead>
          <tbody>
            {filas_alertas if filas_alertas else sin_alertas}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</html>
"""

components.html(html_dashboard, height=800, scrolling=True)