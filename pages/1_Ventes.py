import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Ventes / Caisse",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

html_ventas = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIZZA TIFOSI - Ventes / Caisse</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/litepicker/dist/css/litepicker.css"/>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/litepicker/dist/litepicker.js"></script>
  <style>
    body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1e293b; margin: 0; padding: 0; }
    .main-content { margin-left: 0; padding: 2rem; }
    .header-card, .table-card { background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem; }
    
    .date-picker-btn {
      background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.45rem 0.85rem;
      font-size: 0.85rem; font-weight: 600; color: #334155; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem;
    }
    
    .status-select {
      border-radius: 20px; font-weight: 700; font-size: 0.8rem; padding: 0.3rem 0.8rem; border: 1px solid transparent; cursor: pointer;
    }
    .status-oui { background-color: #dcfce7; color: #15803d; border-color: #bbf7d0; }
    .status-non { background-color: #fee2e2; color: #b91c1c; border-color: #fecaca; }
  </style>
</head>
<body>

  <div class="main-content">
    
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-cart3 text-warning me-2"></i>Gestion des Ventes & Caisse</h3>
        <p class="text-muted m-0 small mt-1">Suivi quotidien des encaissements et calcul automatique du royalty (3%)</p>
      </div>
      
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-warning fw-bold btn-sm shadow-sm px-3" data-bs-toggle="modal" data-bs-target="#modalNouvelleJournee">
          <i class="bi bi-plus-circle-fill me-1"></i> Nouvelle Journée
        </button>

        <button class="date-picker-btn" id="select-dates-btn">
          <i class="bi bi-calendar-range text-warning"></i>
          <span id="date-range-text">07/11/2026</span>
          <i class="bi bi-chevron-down text-muted ms-1" style="font-size: 0.75rem;"></i>
        </button>
      </div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-journal-text me-2 text-primary"></i>Journal des Ventes</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small" id="tabla-ventas">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Espèces</th>
              <th>Carte Bancaire</th>
              <th>Livraison</th>
              <th class="table-primary text-primary">Total Ventes</th>
              <th class="table-danger text-danger">Redevance (3%)</th>
              <th class="text-center">Statut Réserve</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="fw-bold">16/10/2026</td>
              <td>5000.00 €</td>
              <td>4000.00 €</td>
              <td>5000.00 €</td>
              <td class="fw-bold text-primary">14000.00 €</td>
              <td class="fw-bold text-danger">420.00 €</td>
              <td class="text-center">
                <select class="status-select status-oui" onchange="actualizarColor(this)">
                  <option value="Oui" selected>Oui</option>
                  <option value="Non">Non</option>
                </select>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr>
              <td class="fw-bold">15/10/2026</td>
              <td>5000.00 €</td>
              <td>6000.00 €</td>
              <td>7000.00 €</td>
              <td class="fw-bold text-primary">18000.00 €</td>
              <td class="fw-bold text-danger">540.00 €</td>
              <td class="text-center">
                <select class="status-select status-non" onchange="actualizarColor(this)">
                  <option value="Oui">Oui</option>
                  <option value="Non" selected>Non</option>
                </select>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr>
              <td class="fw-bold">23/10/2026</td>
              <td>1999.00 €</td>
              <td>2000.00 €</td>
              <td>1000.00 €</td>
              <td class="fw-bold text-primary">4999.00 €</td>
              <td class="fw-bold text-danger">149.97 €</td>
              <td class="text-center">
                <select class="status-select status-oui" onchange="actualizarColor(this)">
                  <option value="Oui" selected>Oui</option>
                  <option value="Non">Non</option>
                </select>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr>
              <td class="fw-bold">01/11/2026</td>
              <td>9000.00 €</td>
              <td>5000.00 €</td>
              <td>4000.00 €</td>
              <td class="fw-bold text-primary">18000.00 €</td>
              <td class="fw-bold text-danger">540.00 €</td>
              <td class="text-center">
                <select class="status-select status-non" onchange="actualizarColor(this)">
                  <option value="Oui">Oui</option>
                  <option value="Non" selected>Non</option>
                </select>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <!-- Modal Nueva Jornada -->
  <div class="modal fade" id="modalNouvelleJournee" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-plus-circle-fill text-warning me-2"></i>Nouvelle Journée de Vente</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-journee">
            <div class="mb-3">
              <label class="form-label small fw-bold">Date</label>
              <input type="date" id="input-date" class="form-control" value="2026-11-07">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-4">
                <label class="form-label small fw-bold">Espèces (€)</label>
                <input type="number" id="input-especes" class="form-control" placeholder="0" oninput="calcularTotalesNuevo()">
              </div>
              <div class="col-4">
                <label class="form-label small fw-bold">Carte (€)</label>
                <input type="number" id="input-carte" class="form-control" placeholder="0" oninput="calcularTotalesNuevo()">
              </div>
              <div class="col-4">
                <label class="form-label small fw-bold">Livraison (€)</label>
                <input type="number" id="input-livraison" class="form-control" placeholder="0" oninput="calcularTotalesNuevo()">
              </div>
            </div>
            <div class="p-3 bg-light rounded-3 mb-3">
              <div class="d-flex justify-content-between mb-1">
                <span class="small text-muted">Total Ventes:</span>
                <span class="fw-bold text-primary" id="text-total">0.00 €</span>
              </div>
              <div class="d-flex justify-content-between">
                <span class="small text-muted">Redevance Franchise (3%):</span>
                <span class="fw-bold text-danger" id="text-redevance">0.00 €</span>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Statut Réserve</label>
              <select id="input-statut" class="form-select">
                <option value="Oui">Oui (Montant réservé)</option>
                <option value="Non" selected>Non (En attente)</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-light btn-sm fw-bold" data-bs-dismiss="modal">Annuler</button>
          <button type="button" class="btn btn-warning btn-sm fw-bold text-dark px-4" onclick="guardarRegistro()"><i class="bi bi-check-lg me-1"></i> Enregistrer</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Modificar Jornada -->
  <div class="modal fade" id="modalEditarJournee" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-pencil-square text-primary me-2"></i>Modifier la Journée</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-editar">
            <div class="mb-3">
              <label class="form-label small fw-bold">Date</label>
              <input type="text" id="edit-date" class="form-control" readonly>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-4">
                <label class="form-label small fw-bold">Espèces (€)</label>
                <input type="number" id="edit-especes" class="form-control" oninput="calcularTotalesEditar()">
              </div>
              <div class="col-4">
                <label class="form-label small fw-bold">Carte (€)</label>
                <input type="number" id="edit-carte" class="form-control" oninput="calcularTotalesEditar()">
              </div>
              <div class="col-4">
                <label class="form-label small fw-bold">Livraison (€)</label>
                <input type="number" id="edit-livraison" class="form-control" oninput="calcularTotalesEditar()">
              </div>
            </div>
            <div class="p-3 bg-light rounded-3 mb-3">
              <div class="d-flex justify-content-between mb-1">
                <span class="small text-muted">Total Ventes:</span>
                <span class="fw-bold text-primary" id="edit-text-total">0.00 €</span>
              </div>
              <div class="d-flex justify-content-between">
                <span class="small text-muted">Redevance Franchise (3%):</span>
                <span class="fw-bold text-danger" id="edit-text-redevance">0.00 €</span>
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-light btn-sm fw-bold" data-bs-dismiss="modal">Annuler</button>
          <button type="button" class="btn btn-primary btn-sm fw-bold px-4" onclick="guardarEdicion()"><i class="bi bi-check-lg me-1"></i> Mettre à jour</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentRowToEdit = null;

    const picker = new Litepicker({
      element: document.getElementById('select-dates-btn'),
      singleMode: true,
      format: 'DD/MM/YYYY',
      startDate: '2026-11-07',
      setup: (picker) => {
        picker.on('selected', (date1) => {
          document.getElementById('date-range-text').innerText = date1.format('DD/MM/YYYY');
        });
      }
    });

    function actualizarColor(selectElement) {
      if (selectElement.value === 'Oui') {
        selectElement.className = 'status-select status-oui';
      } else {
        selectElement.className = 'status-select status-non';
      }
    }

    function calcularTotalesNuevo() {
      const esp = parseFloat(document.getElementById('input-especes').value) || 0;
      const cb = parseFloat(document.getElementById('input-carte').value) || 0;
      const liv = parseFloat(document.getElementById('input-livraison').value) || 0;
      const total = esp + cb + liv;
      const redevance = total * 0.03;

      document.getElementById('text-total').innerText = total.toFixed(2) + ' €';
      document.getElementById('text-redevance').innerText = redevance.toFixed(2) + ' €';
    }

    function calcularTotalesEditar() {
      const esp = parseFloat(document.getElementById('edit-especes').value) || 0;
      const cb = parseFloat(document.getElementById('edit-carte').value) || 0;
      const liv = parseFloat(document.getElementById('edit-livraison').value) || 0;
      const total = esp + cb + liv;
      const redevance = total * 0.03;

      document.getElementById('edit-text-total').innerText = total.toFixed(2) + ' €';
      document.getElementById('edit-text-redevance').innerText = redevance.toFixed(2) + ' €';
    }

    function guardarRegistro() {
      const dateVal = document.getElementById('input-date').value;
      const esp = parseFloat(document.getElementById('input-especes').value) || 0;
      const cb = parseFloat(document.getElementById('input-carte').value) || 0;
      const liv = parseFloat(document.getElementById('input-livraison').value) || 0;
      const statut = document.getElementById('input-statut').value;

      const total = esp + cb + liv;
      const redevance = total * 0.03;

      if(total === 0) {
        alert("Veuillez saisir au moins un montant.");
        return;
      }

      const statusClass = statut === 'Oui' ? 'status-oui' : 'status-non';
      const tbody = document.querySelector('#tabla-ventas tbody');
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td class="fw-bold">${dateVal.split('-').reverse().join('/')}</td>
        <td>${esp.toFixed(2)} €</td>
        <td>${cb.toFixed(2)} €</td>
        <td>${liv.toFixed(2)} €</td>
        <td class="fw-bold text-primary">${total.toFixed(2)} €</td>
        <td class="fw-bold text-danger">${redevance.toFixed(2)} €</td>
        <td class="text-center">
          <select class="status-select ${statusClass}" onchange="actualizarColor(this)">
            <option value="Oui" ${statut === 'Oui' ? 'selected' : ''}>Oui</option>
            <option value="Non" ${statut === 'Non' ? 'selected' : ''}>Non</option>
          </select>
        </td>
        <td class="text-center">
          <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
          <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
        </td>
      `;

      tbody.insertBefore(newRow, tbody.firstChild);

      const modalEl = document.getElementById('modalNouvelleJournee');
      bootstrap.Modal.getInstance(modalEl).hide();
      document.getElementById('form-journee').reset();
      document.getElementById('text-total').innerText = '0.00 €';
      document.getElementById('text-redevance').innerText = '0.00 €';
    }

    function eliminarFila(btn) {
      if(confirm("Voulez-vous vraiment supprimer cet enregistrement ?")) {
        btn.closest('tr').remove();
      }
    }

    function abrirModalEditar(btn) {
      currentRowToEdit = btn.closest('tr');
      const date = currentRowToEdit.cells[0].innerText;
      const esp = parseFloat(currentRowToEdit.cells[1].innerText) || 0;
      const cb = parseFloat(currentRowToEdit.cells[2].innerText) || 0;
      const liv = parseFloat(currentRowToEdit.cells[3].innerText) || 0;

      document.getElementById('edit-date').value = date;
      document.getElementById('edit-especes').value = esp;
      document.getElementById('edit-carte').value = cb;
      document.getElementById('edit-livraison').value = liv;

      calcularTotalesEditar();

      const modal = new bootstrap.Modal(document.getElementById('modalEditarJournee'));
      modal.show();
    }

    function guardarEdicion() {
      if (!currentRowToEdit) return;

      const esp = parseFloat(document.getElementById('edit-especes').value) || 0;
      const cb = parseFloat(document.getElementById('edit-carte').value) || 0;
      const liv = parseFloat(document.getElementById('edit-livraison').value) || 0;
      const total = esp + cb + liv;
      const redevance = total * 0.03;

      currentRowToEdit.cells[1].innerText = esp.toFixed(2) + ' €';
      currentRowToEdit.cells[2].innerText = cb.toFixed(2) + ' €';
      currentRowToEdit.cells[3].innerText = liv.toFixed(2) + ' €';
      currentRowToEdit.cells[4].innerText = total.toFixed(2) + ' €';
      currentRowToEdit.cells[5].innerText = redevance.toFixed(2) + ' €';

      const modalEl = document.getElementById('modalEditarJournee');
      bootstrap.Modal.getInstance(modalEl).hide();
    }
  </script>

</body>
</html>
"""

components.html(html_ventas, height=1300, scrolling=False)