import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Personnel & Paie",
    page_icon="👥",
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

html_personnel = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIZZA TIFOSI - Personnel & Paie</title>
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
    
    .badge-virement { background-color: #f3e8ff; color: #7e22ce; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }
    .badge-especes { background-color: #e0f2fe; color: #0369a1; font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }
  </style>
</head>
<body>

  <div class="main-content">

    <!-- CABECERA IDÉNTICA A INVENTARIO -->
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-people-fill text-warning me-2"></i>Personnel & Paie</h3>
        <p class="text-muted m-0 small mt-1">Gestion des salaires, heures extra et méthodes de paiement</p>
      </div>
      
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-warning fw-bold btn-sm shadow-sm px-3 text-dark" data-bs-toggle="modal" data-bs-target="#modalNouvelEmploye">
          <i class="bi bi-plus-circle-fill me-1"></i> Ajouter un Paiement
        </button>

        <button class="date-picker-btn" id="select-dates-btn">
          <i class="bi bi-calendar-range text-warning"></i>
          <span id="date-range-text">07/11/2026</span>
          <i class="bi bi-chevron-down text-muted ms-1" style="font-size: 0.75rem;"></i>
        </button>
      </div>
    </div>

    <!-- PANEL DE BÚSQUEDA Y FILTROS IDÉNTICO -->
    <div class="header-card py-3">
      <div class="row g-3 align-items-center">
        <div class="col-md-5">
          <div class="input-group input-group-sm">
            <span class="input-group-text bg-white text-muted"><i class="bi bi-search"></i></span>
            <input type="text" id="buscador-empleado" class="form-control" placeholder="Rechercher par nom d'employé..." onkeyup="filtrarTabla()">
          </div>
        </div>
        <div class="col-md-4">
          <select id="filtro-metodo" class="form-select form-select-sm" onchange="filtrarTabla()">
            <option value="">Toutes les méthodes de paiement</option>
            <option value="Virement">Virement</option>
            <option value="Espèces">Espèces</option>
          </select>
        </div>
        <div class="col-md-3 text-md-end">
          <select id="orden-tabla" class="form-select form-select-sm" onchange="ordenarTabla()">
            <option value="0-asc">Nom (A - Z)</option>
            <option value="5-desc">Total Payé (Plus élevé)</option>
            <option value="3-desc">Salaire Base (Plus élevé)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- TABLA -->
    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-wallet2 me-2 text-primary"></i>Registre des Paiements & Salaires</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small" id="tabla-personal">
          <thead class="table-light">
            <tr>
              <th>Nom</th>
              <th>Période</th>
              <th>Date Paiement</th>
              <th>Salaire Base</th>
              <th>Heures Extra</th>
              <th>Total Payé</th>
              <th>Méthode Paiement</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr data-date="2026-11-01">
              <td class="fw-bold">Hacene</td>
              <td>Mois</td>
              <td>01/11/2026</td>
              <td>5000 €</td>
              <td>-</td>
              <td class="fw-bold text-success">5000 €</td>
              <td><span class="badge-virement">Virement</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-date="2026-11-01">
              <td class="fw-bold">Karim</td>
              <td>Mois</td>
              <td>01/11/2026</td>
              <td>5000 €</td>
              <td>-</td>
              <td class="fw-bold text-success">5000 €</td>
              <td><span class="badge-virement">Virement</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-date="2026-10-15">
              <td class="fw-bold">Amel</td>
              <td>Quinzaine</td>
              <td>15/10/2026</td>
              <td>3000 €</td>
              <td>50 €</td>
              <td class="fw-bold text-success">3050 €</td>
              <td><span class="badge-especes">Espèces</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-date="2026-10-16">
              <td class="fw-bold">Wael</td>
              <td>Quinzaine</td>
              <td>16/10/2026</td>
              <td>2500 €</td>
              <td>100 €</td>
              <td class="fw-bold text-success">2600 €</td>
              <td><span class="badge-virement">Virement</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-date="2026-10-15">
              <td class="fw-bold">Yacer</td>
              <td>Quinzaine</td>
              <td>15/10/2026</td>
              <td>2900 €</td>
              <td>90 €</td>
              <td class="fw-bold text-success">2990 €</td>
              <td><span class="badge-especes">Espèces</span></td>
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

  <!-- Modal Nouvel Employé / Paiement -->
  <div class="modal fade" id="modalNouvelEmploye" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-plus-circle-fill text-warning me-2"></i>Ajouter un Paiement Personnel</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-employe">
            <div class="mb-3">
              <label class="form-label small fw-bold">Employé</label>
              <select id="input-nom" class="form-select">
                <option value="Hacene">Hacene</option>
                <option value="Karim">Karim</option>
                <option value="Amel">Amel</option>
                <option value="Wael">Wael</option>
                <option value="Yacer">Yacer</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Période</label>
              <select id="input-periode" class="form-select">
                <option value="Mois">Mois</option>
                <option value="Quinzaine">Quinzaine</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date Paiement</label>
              <input type="date" id="input-date" class="form-control" value="2026-11-07">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-bold">Salaire Base (€)</label>
                <input type="number" id="input-salaire" class="form-control" placeholder="0">
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Heures Extra (€)</label>
                <input type="number" id="input-extra" class="form-control" placeholder="0">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Méthode Paiement</label>
              <select id="input-metodo" class="form-select">
                <option value="Virement">Virement</option>
                <option value="Espèces">Espèces</option>
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

  <!-- Modal Modifier Paiement (CORREGIDO Y FUNCIONAL) -->
  <div class="modal fade" id="modalEditarEmploye" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-pencil-square text-primary me-2"></i>Modifier le Paiement</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-editar">
            <div class="mb-3">
              <label class="form-label small fw-bold">Employé</label>
              <select id="edit-nom" class="form-select">
                <option value="Hacene">Hacene</option>
                <option value="Karim">Karim</option>
                <option value="Amel">Amel</option>
                <option value="Wael">Wael</option>
                <option value="Yacer">Yacer</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Période</label>
              <select id="edit-periode" class="form-select">
                <option value="Mois">Mois</option>
                <option value="Quinzaine">Quinzaine</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date Paiement</label>
              <input type="date" id="edit-date" class="form-control">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-bold">Salaire Base (€)</label>
                <input type="number" id="edit-salaire" class="form-control">
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Heures Extra (€)</label>
                <input type="number" id="edit-extra" class="form-control">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Méthode Paiement</label>
              <select id="edit-metodo" class="form-select">
                <option value="Virement">Virement</option>
                <option value="Espèces">Espèces</option>
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
      const texto = document.getElementById('buscador-empleado').value.toLowerCase();
      const metodo = document.getElementById('filtro-metodo').value;
      const filas = document.querySelectorAll('#tabla-personal tbody tr');

      filas.forEach(fila => {
        const nombre = fila.cells[0].innerText.toLowerCase();
        const badgeVal = fila.cells[6].innerText.trim();

        const coincideTexto = nombre.includes(texto);
        const coincideMetodo = (metodo === "" || badgeVal === metodo);

        if (coincideTexto && coincideMetodo) {
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
      
      const tbody = document.querySelector('#tabla-personal tbody');
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
      const nom = document.getElementById('input-nom').value;
      const periode = document.getElementById('input-periode').value;
      const fechaIso = document.getElementById('input-date').value;
      const salaire = parseFloat(document.getElementById('input-salaire').value) || 0;
      const extra = parseFloat(document.getElementById('input-extra').value) || 0;
      const metodo = document.getElementById('input-metodo').value;

      if(!fechaIso) {
        alert("Veuillez sélectionner une date.");
        return;
      }

      const fechaFormatted = fechaIso.split('-').reverse().join('/');
      const total = salaire + extra;
      const badgeClass = metodo === 'Virement' ? 'badge-virement' : 'badge-especes';

      const tbody = document.querySelector('#tabla-personal tbody');
      const newRow = document.createElement('tr');
      newRow.setAttribute('data-date', fechaIso);
      newRow.innerHTML = `
        <td class="fw-bold">${nom}</td>
        <td>${periode}</td>
        <td>${fechaFormatted}</td>
        <td>${salaire} €</td>
        <td>${extra > 0 ? extra + ' €' : '-'}</td>
        <td class="fw-bold text-success">${total} €</td>
        <td><span class="${badgeClass}">${metodo}</span></td>
        <td class="text-center">
          <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
          <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
        </td>
      `;

      tbody.insertBefore(newRow, tbody.firstChild);
      
      const modalEl = document.getElementById('modalNouvelEmploye');
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
      
      document.getElementById('form-employe').reset();
    }

    function abrirModalEditar(btn) {
      currentRowToEdit = btn.closest('tr');
      const nom = currentRowToEdit.cells[0].innerText.trim();
      const periode = currentRowToEdit.cells[1].innerText.trim();
      const salaireStr = currentRowToEdit.cells[3].innerText.replace('€', '').trim();
      const extraStr = currentRowToEdit.cells[4].innerText.replace('€', '').replace('-', '0').trim();
      const metodo = currentRowToEdit.cells[6].innerText.trim();
      const fechaIso = currentRowToEdit.getAttribute('data-date') || '2026-11-01';

      document.getElementById('edit-nom').value = nom;
      document.getElementById('edit-periode').value = periode;
      document.getElementById('edit-date').value = fechaIso;
      document.getElementById('edit-salaire').value = parseFloat(salaireStr) || 0;
      document.getElementById('edit-extra').value = parseFloat(extraStr) || 0;
      document.getElementById('edit-metodo').value = metodo;

      new bootstrap.Modal(document.getElementById('modalEditarEmploye')).show();
    }

    function guardarEdicion() {
      if(!currentRowToEdit) return;

      const nom = document.getElementById('edit-nom').value;
      const periode = document.getElementById('edit-periode').value;
      const fechaIso = document.getElementById('edit-date').value;
      const salaire = parseFloat(document.getElementById('edit-salaire').value) || 0;
      const extra = parseFloat(document.getElementById('edit-extra').value) || 0;
      const metodo = document.getElementById('edit-metodo').value;

      const fechaFormatted = fechaIso.split('-').reverse().join('/');
      const total = salaire + extra;
      const badgeClass = metodo === 'Virement' ? 'badge-virement' : 'badge-especes';

      currentRowToEdit.setAttribute('data-date', fechaIso);
      currentRowToEdit.cells[0].innerText = nom;
      currentRowToEdit.cells[1].innerText = periode;
      currentRowToEdit.cells[2].innerText = fechaFormatted;
      currentRowToEdit.cells[3].innerText = salaire + ' €';
      currentRowToEdit.cells[4].innerText = extra > 0 ? extra + ' €' : '-';
      currentRowToEdit.cells[5].innerText = total + ' €';
      currentRowToEdit.cells[6].innerHTML = `<span class="${badgeClass}">${metodo}</span>`;

      const modalEl = document.getElementById('modalEditarEmploye');
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

components.html(html_personnel, height=1300, scrolling=False)