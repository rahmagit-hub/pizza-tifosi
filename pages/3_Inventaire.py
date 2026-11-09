import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Inventaire & Stocks",
    page_icon="📦",
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

html_inventaire = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIZZA TIFOSI - Inventaire & Stocks</title>
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
    
    .cat-badge { font-weight: 600; font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 20px; }
    .cat-fromage { background-color: #f3e8ff; color: #7e22ce; }
    .cat-viande { background-color: #e0f2fe; color: #0369a1; }
    .cat-boisson { background-color: #ffedd5; color: #c2410c; }

    .alert-ok { background-color: #dcfce7; color: #15803d; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.6rem; border-radius: 20px; display: inline-block; }
    
    @keyframes parpadeoAlerta {
      0% { background-color: #fee2e2; transform: scale(1); }
      50% { background-color: #fecaca; transform: scale(1.02); box-shadow: 0 0 10px rgba(220, 38, 38, 0.4); }
      100% { background-color: #fee2e2; transform: scale(1); }
    }
    .alert-proche { 
      background-color: #fee2e2; 
      color: #b91c1c; 
      font-weight: 800; 
      font-size: 0.75rem; 
      padding: 0.4rem 0.8rem; 
      border-radius: 20px; 
      display: inline-block;
      animation: parpadeoAlerta 1.2s infinite ease-in-out;
      border: 1px solid #f87171;
    }
  </style>
</head>
<body>

  <div class="main-content">

    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-box-seam text-warning me-2"></i>Inventaire & Stocks</h3>
        <p class="text-muted m-0 small mt-1">Gestion des stocks de produits, unités et suivi des dates de péremption</p>
      </div>
      
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-warning fw-bold btn-sm shadow-sm px-3" data-bs-toggle="modal" data-bs-target="#modalNouvelArticle">
          <i class="bi bi-plus-circle-fill me-1"></i> Nouvel Article
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
            <input type="text" id="buscador-producto" class="form-control" placeholder="Rechercher par nom de produit..." onkeyup="filtrarTabla()">
          </div>
        </div>
        <div class="col-md-4">
          <select id="filtro-categoria" class="form-select form-select-sm" onchange="filtrarTabla()">
            <option value="">Toutes les catégories</option>
            <option value="Fromage">Fromage</option>
            <option value="Viande">Viande</option>
            <option value="Boisson">Boisson</option>
          </select>
        </div>
        <div class="col-md-3 text-md-end">
          <select id="orden-tabla" class="form-select form-select-sm" onchange="ordenarTabla()">
            <option value="0-asc">Nom (A - Z)</option>
            <option value="0-desc">Nom (Z - A)</option>
            <option value="2-desc">Stock (Plus élevé)</option>
            <option value="5-asc">Jours Restants (Urgent)</option>
          </select>
        </div>
      </div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-clipboard-data me-2 text-primary"></i>État des Stocks & Péremptions</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small" id="tabla-inventario">
          <thead class="table-light">
            <tr>
              <th>Nom du Produit</th>
              <th>Catégorie</th>
              <th>Stock Actuel</th>
              <th>Unité</th>
              <th>Date d'expiration</th>
              <th class="text-center">Jours Restants</th>
              <th>Expiration Proche</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr data-exp="2026-11-28">
              <td class="fw-bold">Mozzarella</td>
              <td><span class="cat-badge cat-fromage">Fromage</span></td>
              <td class="fw-bold">20</td>
              <td>Boite</td>
              <td>28/11/2026</td>
              <td class="text-center fw-bold jours-restantes">21</td>
              <td><span class="alert-ok">OK</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-exp="2026-11-10">
              <td class="fw-bold">Cheddar</td>
              <td><span class="cat-badge cat-fromage">Fromage</span></td>
              <td class="fw-bold">14</td>
              <td>Boite</td>
              <td>10/11/2026</td>
              <td class="text-center fw-bold text-danger">3</td>
              <td><span class="alert-proche">🚨 PROCHE EXPIRATION</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-exp="2026-11-09">
              <td class="fw-bold">Viande Hachée</td>
              <td><span class="cat-badge cat-viande">Viande</span></td>
              <td class="fw-bold">12</td>
              <td>Kg</td>
              <td>09/11/2026</td>
              <td class="text-center fw-bold text-danger">2</td>
              <td><span class="alert-proche">🚨 PROCHE EXPIRATION</span></td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>
            <tr data-exp="2026-11-05">
              <td class="fw-bold">Fanta Orange</td>
              <td><span class="cat-badge cat-boisson">Boisson</span></td>
              <td class="fw-bold">14</td>
              <td>Unité</td>
              <td>05/11/2026</td>
              <td class="text-center fw-bold text-danger">-2</td>
              <td><span class="alert-proche">🚨 CADUCÉ / EXPIRÉ</span></td>
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

  <!-- Modal Nouvel Article -->
  <div class="modal fade" id="modalNouvelArticle" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-plus-circle-fill text-warning me-2"></i>Ajouter un Article</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-article">
            <div class="mb-3">
              <label class="form-label small fw-bold">Nom du Produit</label>
              <input type="text" id="input-nom" class="form-control" placeholder="Ex: Mozzarella, Coca...">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Catégorie</label>
              <select id="input-cat" class="form-select">
                <option value="Fromage">Fromage</option>
                <option value="Viande">Viande</option>
                <option value="Boisson">Boisson</option>
              </select>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-bold">Stock Actuel</label>
                <input type="number" id="input-stock" class="form-control" placeholder="0">
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Unité</label>
                <select id="input-unite" class="form-select">
                  <option value="Boite">Boite</option>
                  <option value="Kg">Kg</option>
                  <option value="Unité">Unité</option>
                </select>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date d'expiration</label>
              <input type="date" id="input-exp" class="form-control" value="2026-11-20">
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

  <!-- Modal Modifier Article -->
  <div class="modal fade" id="modalEditarArticle" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-pencil-square text-primary me-2"></i>Modifier l'Article</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-editar">
            <div class="mb-3">
              <label class="form-label small fw-bold">Nom du Produit</label>
              <input type="text" id="edit-nom" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Catégorie</label>
              <select id="edit-cat" class="form-select">
                <option value="Fromage">Fromage</option>
                <option value="Viande">Viande</option>
                <option value="Boisson">Boisson</option>
              </select>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-bold">Stock Actuel</label>
                <input type="number" id="edit-stock" class="form-control">
              </div>
              <div class="col-6">
                <label class="form-label small fw-bold">Unité</label>
                <select id="edit-unite" class="form-select">
                  <option value="Boite">Boite</option>
                  <option value="Kg">Kg</option>
                  <option value="Unité">Unité</option>
                </select>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Date d'expiration</label>
              <input type="date" id="edit-exp" class="form-control">
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
    const fechaActual = new Date('2026-11-07');

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

    function calcularDias(expDateStr) {
      const expDate = new Date(expDateStr);
      const diffTime = expDate - fechaActual;
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    function filtrarTabla() {
      const texto = document.getElementById('buscador-producto').value.toLowerCase();
      const categoria = document.getElementById('filtro-categoria').value;
      const filas = document.querySelectorAll('#tabla-inventario tbody tr');

      filas.forEach(fila => {
        const nombre = fila.cells[0].innerText.toLowerCase();
        const catBadge = fila.cells[1].innerText.trim();

        const coincideTexto = nombre.includes(texto);
        const coincideCat = (categoria === "" || catBadge === categoria);

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
      
      const tbody = document.querySelector('#tabla-inventario tbody');
      const filas = Array.from(tbody.querySelectorAll('tr'));

      filas.sort((a, b) => {
        let valA = a.cells[colIndex].innerText.trim();
        let valB = b.cells[colIndex].innerText.trim();

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
      const nom = document.getElementById('input-nom').value || 'Produit';
      const cat = document.getElementById('input-cat').value;
      const stock = document.getElementById('input-stock').value || '0';
      const unite = document.getElementById('input-unite').value;
      const exp = document.getElementById('input-exp').value;

      if(!exp) {
        alert("Veuillez sélectionner une date d'expiration.");
        return;
      }

      const dias = calcularDias(exp);
      const catClass = cat === 'Fromage' ? 'cat-fromage' : (cat === 'Viande' ? 'cat-viande' : 'cat-boisson');
      
      let alertHtml = '<span class="alert-ok">OK</span>';
      let diasClass = 'text-center fw-bold jours-restantes';
      if(dias <= 5) {
        alertHtml = '<span class="alert-proche">🚨 PROCHE EXPIRATION</span>';
        diasClass = 'text-center fw-bold text-danger';
      }

      const tbody = document.querySelector('#tabla-inventario tbody');
      const newRow = document.createElement('tr');
      newRow.setAttribute('data-exp', exp);
      newRow.innerHTML = `
        <td class="fw-bold">${nom}</td>
        <td><span class="cat-badge ${catClass}">${cat}</span></td>
        <td class="fw-bold">${stock}</td>
        <td>${unite}</td>
        <td>${exp.split('-').reverse().join('/')}</td>
        <td class="${diasClass}">${dias}</td>
        <td>${alertHtml}</td>
        <td class="text-center">
          <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
          <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
        </td>
      `;

      tbody.insertBefore(newRow, tbody.firstChild);
      
      const modalEl = document.getElementById('modalNouvelArticle');
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
      
      document.getElementById('form-article').reset();
    }

    function abrirModalEditar(btn) {
      currentRowToEdit = btn.closest('tr');
      const nom = currentRowToEdit.cells[0].innerText;
      const cat = currentRowToEdit.cells[1].querySelector('.cat-badge').innerText.trim();
      const stock = currentRowToEdit.cells[2].innerText;
      const unite = currentRowToEdit.cells[3].innerText;
      const expIso = currentRowToEdit.getAttribute('data-exp');

      document.getElementById('edit-nom').value = nom;
      document.getElementById('edit-cat').value = cat;
      document.getElementById('edit-stock').value = stock;
      document.getElementById('edit-unite').value = unite;
      document.getElementById('edit-exp').value = expIso;

      new bootstrap.Modal(document.getElementById('modalEditarArticle')).show();
    }

    function guardarEdicion() {
      if(!currentRowToEdit) return;

      const nom = document.getElementById('edit-nom').value;
      const cat = document.getElementById('edit-cat').value;
      const stock = document.getElementById('edit-stock').value;
      const unite = document.getElementById('edit-unite').value;
      const exp = document.getElementById('edit-exp').value;

      const dias = calcularDias(exp);
      const catClass = cat === 'Fromage' ? 'cat-fromage' : (cat === 'Viande' ? 'cat-viande' : 'cat-boisson');
      
      let alertHtml = '<span class="alert-ok">OK</span>';
      let diasClass = 'text-center fw-bold jours-restantes';
      if(dias <= 5) {
        alertHtml = '<span class="alert-proche">🚨 PROCHE EXPIRATION</span>';
        diasClass = 'text-center fw-bold text-danger';
      }

      currentRowToEdit.setAttribute('data-exp', exp);
      currentRowToEdit.cells[0].innerText = nom;
      currentRowToEdit.cells[1].innerHTML = `<span class="cat-badge ${catClass}">${cat}</span>`;
      currentRowToEdit.cells[2].innerText = stock;
      currentRowToEdit.cells[3].innerText = unite;
      currentRowToEdit.cells[4].innerText = exp.split('-').reverse().join('/');
      currentRowToEdit.cells[5].className = diasClass;
      currentRowToEdit.cells[5].innerText = dias;
      currentRowToEdit.cells[6].innerHTML = alertHtml;

      const modalEl = document.getElementById('modalEditarArticle');
      const modalInstance = bootstrap.Modal.getInstance(modalEl);
      if (modalInstance) modalInstance.hide();
    }

    function eliminarFila(btn) {
      if(confirm("Voulez-vous vraiment supprimer cet article ?")) {
        btn.closest('tr').remove();
      }
    }
  </script>

</body>
</html>
"""

components.html(html_inventaire, height=1350, scrolling=False)