import streamlit as st
import streamlit.components.v1 as components
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

html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/litepicker/dist/css/litepicker.css"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/litepicker/dist/litepicker.js"></script>
  <style>
    body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1e293b; margin: 0; padding: 0; }
    .main-content { padding: 2rem; }
    .header-card { background: #ffffff; border-radius: 12px; padding: 1.25rem 1.75rem; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem; }
    .stat-card { background: #ffffff; border-radius: 12px; padding: 1.25rem; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); height: 100%; }
    .stat-value { font-size: 1.8rem; font-weight: 700; color: #0f172a; }
    .stat-label { font-size: 0.875rem; color: #64748b; }
    .chart-card, .table-card { background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem; }
    .date-picker-btn { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.4rem 0.85rem; font-size: 0.85rem; font-weight: 600; color: #334155; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .date-picker-btn:hover { background: #f8fafc; border-color: #94a3b8; }
  </style>
</head>
<body>

  <div class="main-content">
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-bar-chart-fill text-warning me-2"></i>Tableau de Bord</h3>
        <p class="text-muted m-0 small mt-1">Aperçu général des ventes, canaux de paiement et alertes de stock</p>
      </div>
      <button class="date-picker-btn" id="select-dates-btn">
        <i class="bi bi-calendar-range text-warning"></i>
        <span id="date-range-text">01/11/2026 - 07/11/2026</span>
        <i class="bi bi-chevron-down text-muted ms-1" style="font-size: 0.75rem;"></i>
      </button>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Ventes Totales</div><div class="stat-value">1 420.00 €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Redevance Franchise (3%)</div><div class="stat-value text-danger">42.60 €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Achats Totaux</div><div class="stat-value">380.50 €</div></div></div>
      <div class="col-md-3"><div class="stat-card"><div class="stat-label">Alertes Péremption</div><div class="stat-value text-warning">2 produits</div></div></div>
    </div>

    <div class="row">
      <div class="col-md-7">
        <div class="chart-card">
          <h6 class="fw-bold mb-3"><i class="bi bi-graph-up-arrow me-2 text-success"></i>Évolution des Ventes Totales</h6>
          <canvas id="salesChart" height="150"></canvas>
        </div>
      </div>
      <div class="col-md-5">
        <div class="chart-card">
          <h6 class="fw-bold mb-3"><i class="bi bi-pie-chart-fill me-2 text-warning"></i>Répartition par Mode de Paiement</h6>
          <canvas id="paymentsChart" height="180"></canvas>
        </div>
      </div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-exclamation-triangle-fill me-2 text-danger"></i>Alertes de Péremption (Prochains à caducar)</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small">
          <thead class="table-light">
            <tr><th>Produit</th><th>Quantité</th><th>Date de Péremption</th><th>Statut</th></tr>
          </thead>
          <tbody>
            <tr><td class="fw-bold">Mozzarella Fraîche</td><td>4.5 kg</td><td>09/11/2026</td><td><span class="badge bg-danger">🔴 Urgent (2 jours)</span></td></tr>
            <tr><td class="fw-bold">Pâte à Pizza (Boules)</td><td>18 unités</td><td>10/11/2026</td><td><span class="badge bg-danger">🔴 Urgent (3 jours)</span></td></tr>
            <tr><td class="fw-bold">Jambon Blanc</td><td>2.2 kg</td><td>12/11/2026</td><td><span class="badge bg-warning text-dark">🟠 Attention</span></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    const picker = new Litepicker({
      element: document.getElementById('select-dates-btn'),
      singleMode: false,
      numberOfMonths: 2,
      numberOfColumns: 2,
      format: 'DD/MM/YYYY',
      startDate: '2026-11-01',
      endDate: '2026-11-07',
      setup: (picker) => {
        picker.on('selected', (date1, date2) => {
          document.getElementById('date-range-text').innerText = `${date1.format('DD/MM/YYYY')} - ${date2.format('DD/MM/YYYY')}`;
        });
      }
    });

    new Chart(document.getElementById('salesChart').getContext('2d'), {
      type: 'line',
      data: {
        labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        datasets: [{ label: 'Ventes (€)', data: [150, 210, 180, 260, 390, 510, 420], borderColor: '#ea580c', backgroundColor: 'rgba(234, 88, 12, 0.1)', fill: true, tension: 0.3 }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });

    new Chart(document.getElementById('paymentsChart').getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Carte (CB)', 'Livraison (Uber/Glovo)', 'Espèces'],
        datasets: [{ data: [52, 33, 15], backgroundColor: ['#2563eb', '#f59e0b', '#10b981'] }]
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  </script>

</body>
</html>
"""

components.html(html_code, height=1400, scrolling=False)