import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Charges Fixes",
    page_icon="🧾",
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

html_charges = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIZZA TIFOSI - Charges Fixes</title>
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
    
    .badge-loyer { background-color: #e0f2fe; color: #0369a1; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }
    .badge-electricite { background-color: #fef3c7; color: #d97706; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }
    .badge-eau { background-color: #f3e8ff; color: #7e22ce; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }

    .badge-paye { background-color: #dcfce7; color: #15803d; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; display: inline-block; }
    .badge-attente { background-color: #fee2e2; color: #b91c1c; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; display: inline-block; }
  </style>
</head>
<body>

  <div class="main-content">

    <!-- CABECERA -->
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-receipt text-warning me-2"></i>Charges Fixes</h3>
        <p class="text-muted m-0 small mt-1">Gestion des dépenses fixes, loyers, factures et abonnements</p>
      </div>
      
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-warning fw-bold btn-sm shadow-sm px-3 text-dark" data-bs-toggle="modal" data-bs-target="#modalNouvelleCharge">
          <i class="bi bi-plus-circle-fill me-1"></i> Nouvelle Charge
        </button>

        <button class="date-picker-btn" id="select-dates-btn">
          <i class="bi bi-calendar-range text-warning"></i>
          <span id="date-range-text">07/11/2026</span>
          <i class="bi bi-chevron-down text-muted ms-1" style="font-size: 0.75rem;"></i>
        </button>
      </div>
    </div>

    <!-- PANEL DE BÚSQUEDA Y FILTROS -->
    <div class="header-card py-3">
      <div class="row g-3 align-items-center">
        <div class="col-md-5">
          <div class="input-group input-group-sm">
            <span class="input-group-text bg-white text-muted"><i class="bi bi-search"></i></span>
            <input type="text" id="buscador-charge" class="form-control" placeholder="Rechercher par catégorie..." onkeyup="filtrarTabla()">
          </div>
        </div>
        <div class="col-md-4">
          <select id="filtro-categoria" class="form-select form-select-sm" onchange="filtrarTabla()">
            <option value="">Toutes les catégories</option>
            <option value="Loyer">Loyer</option>
            <option value="Électricité">Électricité</option>
            <option value="Eau">Eau</option>
          </select>
        </div>
        <div class="col-md-3 text-md-end">
          <select id="orden-tabla" class="form-select form-select-sm" onchange="ordenarTabla()">
            <option value="2-desc">Montant (Plus élevé)</option>
            <option value="2-asc">Montant (Moins élevé)</option>
            <option value="0-desc">Mois (Récent)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- TABLA -->
    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-clipboard-data me-2 text-primary"></i>Registre des Charges Fixes</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small" id="tabla-charges">
          <thead class="table-light">
            <tr>
              <th>Mois</th>
              <th>Catégorie de Charge</th>
              <th>Montant</th>
              <th>Date de Paiement</th>
              <th>Statut</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr data-mois="2026-11-01" data-pago="2026-11-02">
              <td>01/11/2026</td>
              <td><span class="badge-loyer">Loyer</span></td>
              <td class="fw-bold text-danger">1000 €</td>
              <td>02/11/2026</td>
              <td><span class="badge-paye">Payé</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-mois="2026-10-01" data-pago="2026-10-03">
              <td>01/10/2026</td>
              <td><span class="badge-electricite">Électricité</span></td>
              <td class="fw-bold text-danger">30 €</td>
              <td>03/10/2026</td>
              <td><span class="badge-paye">Payé</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-mois="2026-09-01" data-pago="">
              <td>01/09/2026</td>
              <td><span class="badge-eau">Eau</span></td>
              <td class="fw-bold text-danger">200 €</td>
              <td>-</td>
              <td><span class="badge-attente">En att...</span></td>
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

  <!-- Modal Nueva Charge -->
  <div class="modal fade" id="modalNouvelleCharge" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-plus-circle-fill text-warning me-2"></i>Ajouter une Charge</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-charge">
            <div class="mb-3">
              <label class="form-label small fw-bold">Mois</label>
              <input type="date" id="input-mois" class="form-control" value="2026-11-01">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Catégorie de Charge</label>
              <select id="input-cat" class="form-select">
                <option value="Loyer">Loyer</option>
                <option value="Électricité">Électricité</option>
                <option value="Eau">Eau</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Montant (€)</label>
              <input type="number" id="input-montant" class="form-control" placeholder="0">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date de Paiement</label>
              <input type="date" id="input-pago" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Statut</label>
              <select id="input-statut" class="form-select">
                <option value="Payé">Payé</option>
                <option value="En att...">En att...</option>
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

  <!-- Modal Modifier Charge -->
  <div class="modal fade" id="modalEditarCharge" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-pencil-square text-primary me-2"></i>Modifier la Charge</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-editar">
            <div class="mb-3">
              <label class="form-label small fw-bold">Mois</label>
              <input type="date" id="edit-mois" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Catégorie de Charge</label>
              <select id="edit-cat" class="form-select">
                <option value="Loyer">Loyer</option>
                <option value="Électricité">Électricité</option>
                <option value="Eau">Eau</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Montant (€)</label>
              <input type="number" id="edit-montant" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date de Paiement</label>
              <input type="date" id="edit-pago" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Statut</label>
              <select id="edit-statut" class="form-select">
                <option value="Payé">Payé</option>
                <option value="En att...">En att...</option>
              </select>
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

    function filtrarTabla() {
      const texto = document.getElementById('buscador-charge').value.toLowerCase();
      const categoria = document.getElementById('filtro-categoria').value;
      const filas = document.querySelectorAll('#tabla-charges tbody tr');

      filas.forEach(fila => {
        const catText = fila.cells[1].innerText.toLowerCase();
        const catVal = fila.cells[1].innerText.trim();

        const coincideTexto = catText.includes(texto);
        const coincideCat = (categoria === "" || catVal === categoria);

        if (coincideTexto && coincideCat) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    }

    function ordenarTabla() {
      const selectVal = document.getElementById('orden-tabla').value.split('-');
      const colIndex = parseInt(selectVal[0]);
      const direccion = selectVal[1];
      
      const tbody = document.querySelector('#tabla-charges tbody');
      const filas = Array.from(tbody.querySelectorAll('tr'));

      filas.sort((a, b) => {
        let valA = a.cells[colIndex].innerText.replace('€', '').trim();
        let valB = b.cells[colIndex].innerText.replace('€', '').trim();

        if (!isNaN(valA) && !isNaN(valB)) {
          valA = parseFloat(valA);
          valB = parseFloat(valB);
        }

        if (direccion === 'asc') {
          return valA > valB ? 1 : -1;
        } else {
          return valA < valB ? 1 : -1;
        }
      });

      filas.forEach(fila => tbody.appendChild(fila));
    }

    function guardarRegistro() {
      const moisIso = document.getElementById('input-mois').value;
      const cat = document.getElementById('input-cat').value;
      const montant = parseFloat(document.getElementById('input-montant').value) || 0;
      const pagoIso = document.getElementById('input-pago').value;
      const statut = document.getElementById('input-statut').value;

      if(!moisIso) {
        alert("Veuillez sélectionner le mois.");
        return;
      }

      const moisFormatted = moisIso.split('-').reverse().join('/');
      const pagoFormatted = pagoIso ? pagoIso.split('-').reverse().join('/') : '-';
      
      const badgeCatClass = cat === 'Loyer' ? 'badge-loyer' : (cat === 'Électricité' ? 'badge-electricite' : 'badge-eau');
      const badgeStatutClass = statut === 'Payé' ? 'badge-paye' : 'badge-attente';

      const tbody = document.querySelector('#tabla-charges tbody');
      const newRow = document.createElement('tr');
      newRow.setAttribute('data-mois', moisIso);
      newRow.setAttribute('data-pago', pagoIso || '');
      newRow.innerHTML = `
        <td>${moisFormatted}</td>
        <td><span class="${badgeCatClass}">${cat}</span></td>
        <td class="fw-bold text-danger">${montant} €</td>
        <td>${pagoFormatted}</td>
        <td><span class="${badgeStatutClass}">${statut}</span></td>
        <td class="text-center">
          <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
          <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
        </td>
      `;

      tbody.insertBefore(newRow, tbody.firstChild);
      
      const modalEl = document.getElementById('modalNouvelleCharge');
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
      
      document.getElementById('form-charge').reset();
    }

    function abrirModalEditar(btn) {
      currentRowToEdit = btn.closest('tr');
      const moisIso = currentRowToEdit.getAttribute('data-mois') || '2026-11-01';
      const cat = currentRowToEdit.cells[1].innerText.trim();
      const montantStr = currentRowToEdit.cells[2].innerText.replace('€', '').trim();
      const pagoIso = currentRowToEdit.getAttribute('data-pago') || '';
      const statut = currentRowToEdit.cells[4].innerText.trim();

      document.getElementById('edit-mois').value = moisIso;
      document.getElementById('edit-cat').value = cat;
      document.getElementById('edit-montant').value = parseFloat(montantStr) || 0;
      document.getElementById('edit-pago').value = pagoIso;
      document.getElementById('edit-statut').value = statut;

      new bootstrap.Modal(document.getElementById('modalEditarCharge')).show();
    }

    function guardarEdicion() {
      if(!currentRowToEdit) return;

      const moisIso = document.getElementById('edit-mois').value;
      const cat = document.getElementById('edit-cat').value;
      const montant = parseFloat(document.getElementById('edit-montant').value) || 0;
      const pagoIso = document.getElementById('edit-pago').value;
      const statut = document.getElementById('edit-statut').value;

      const moisFormatted = moisIso.split('-').reverse().join('/');
      const pagoFormatted = pagoIso ? pagoIso.split('-').reverse().join('/') : '-';
      
      const badgeCatClass = cat === 'Loyer' ? 'badge-loyer' : (cat === 'Électricité' ? 'badge-electricite' : 'badge-eau');
      const badgeStatutClass = statut === 'Payé' ? 'badge-paye' : 'badge-attente';

      currentRowToEdit.setAttribute('data-mois', moisIso);
      currentRowToEdit.setAttribute('data-pago', pagoIso || '');
      currentRowToEdit.cells[0].innerText = moisFormatted;
      currentRowToEdit.cells[1].innerHTML = `<span class="${badgeCatClass}">${cat}</span>`;
      currentRowToEdit.cells[2].innerText = montant + ' €';
      currentRowToEdit.cells[3].innerText = pagoFormatted;
      currentRowToEdit.cells[4].innerHTML = `<span class="${badgeStatutClass}">${statut}</span>`;

      const modalEl = document.getElementById('modalEditarCharge');
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
    }

    function eliminarFila(btn) {
      if(confirm("Voulez-vous vraiment supprimer cet enregistrement ?")) {
        btn.closest('tr').remove();
      }
    }
  </script>

</body>
</html>
"""

components.html(html_charges, height=1300, scrolling=False)