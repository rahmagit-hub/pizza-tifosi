import streamlit as st
import streamlit.components.v1 as components
from sidebar import render_sidebar

st.set_page_config(
    page_title="PIZZA TIFOSI - Achats",
    page_icon="🛍️",
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

html_achats = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PIZZA TIFOSI - Achats</title>
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
    
    .prov-badge {
      font-weight: 600; font-size: 0.8rem; padding: 0.3rem 0.8rem; border-radius: 20px;
    }
    .prov-cotsco { background-color: #e0f2fe; color: #0369a1; }
    .prov-fournisseur { background-color: #fae8ff; color: #86198f; }

    .subrow-container {
      background-color: #f8fafc;
      padding: 12px 20px;
      border-left: 3px solid #2563eb;
      border-bottom: 1px solid #e2e8f0;
    }
  </style>
</head>
<body>

  <div class="main-content">
    
    <div class="header-card d-flex justify-content-between align-items-center">
      <div>
        <h3 class="m-0 fw-bold"><i class="bi bi-bag-fill text-warning me-2"></i>Gestion des Achats</h3>
        <p class="text-muted m-0 small mt-1">Suivi des achats, tickets avec appareil photo direct et détail des produits</p>
      </div>
      
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-warning fw-bold btn-sm shadow-sm px-3" data-bs-toggle="modal" data-bs-target="#modalNouvelAchat">
          <i class="bi bi-plus-circle-fill me-1"></i> Nouvel Achat
        </button>

        <button class="date-picker-btn" id="select-dates-btn">
          <i class="bi bi-calendar-range text-warning"></i>
          <span id="date-range-text">07/11/2026</span>
          <i class="bi bi-chevron-down text-muted ms-1" style="font-size: 0.75rem;"></i>
        </button>
      </div>
    </div>

    <div class="table-card">
      <h6 class="fw-bold mb-3"><i class="bi bi-journal-text me-2 text-primary"></i>Journal des Achats</h6>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 small" id="tabla-achats">
          <thead class="table-light">
            <tr>
              <th>Date d'achat</th>
              <th>Provenance</th>
              <th class="table-primary text-primary">Prix Total</th>
              <th class="text-center">Photo Ticket</th>
              <th class="text-center">Détail Produits</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Fila 1 -->
            <tr data-productos='[{"nombre":"Mozzarella","cantidad":"10 kg","precio":"60"}]' data-foto="">
              <td class="fw-bold">10/09/2026</td>
              <td><span class="prov-badge prov-cotsco">Cotsco</span></td>
              <td class="fw-bold text-primary">600.00 €</td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
                  <i class="bi bi-camera-fill text-dark me-1"></i> Photo
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="abrirModalProductos(this)">
                  <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">1</span>)
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>

            <!-- Fila 2 -->
            <tr data-productos='[]' data-foto="">
              <td class="fw-bold">15/09/2026</td>
              <td><span class="prov-badge prov-fournisseur">Fournisseur</span></td>
              <td class="fw-bold text-primary">400.00 €</td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
                  <i class="bi bi-camera-fill text-dark me-1"></i> Photo
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="abrirModalProductos(this)">
                  <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">0</span>)
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>

            <!-- Fila 3 -->
            <tr data-productos='[]' data-foto="">
              <td class="fw-bold">07/10/2026</td>
              <td><span class="prov-badge prov-cotsco">Cotsco</span></td>
              <td class="fw-bold text-primary">700.00 €</td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
                  <i class="bi bi-camera-fill text-dark me-1"></i> Photo
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="abrirModalProductos(this)">
                  <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">0</span>)
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>

            <!-- Fila 4 -->
            <tr data-productos='[]' data-foto="">
              <td class="fw-bold">01/11/2026</td>
              <td><span class="prov-badge prov-fournisseur">Fournisseur</span></td>
              <td class="fw-bold text-primary">500.00 €</td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
                  <i class="bi bi-camera-fill text-dark me-1"></i> Photo
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="abrirModalProductos(this)">
                  <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">0</span>)
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
                <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
              </td>
            </tr>

            <!-- Fila 5 -->
            <tr data-productos='[]' data-foto="">
              <td class="fw-bold">05/11/2026</td>
              <td><span class="prov-badge prov-fournisseur">Fournisseur</span></td>
              <td class="fw-bold text-primary">1000.00 €</td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
                  <i class="bi bi-camera-fill text-dark me-1"></i> Photo
                </button>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="abrirModalProductos(this)">
                  <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">0</span>)
                </button>
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

  <!-- Modal Nouvel Achat -->
  <div class="modal fade" id="modalNouvelAchat" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-plus-circle-fill text-warning me-2"></i>Nouvel Achat</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-achat">
            <div class="mb-3">
              <label class="form-label small fw-bold">Date d'achat</label>
              <input type="date" id="input-date" class="form-control" value="2026-11-07">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Provenance</label>
              <select id="input-provenance" class="form-select">
                <option value="Cotsco">Cotsco</option>
                <option value="Fournisseur">Fournisseur</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Prix Total (€)</label>
              <input type="number" id="input-precio" class="form-control" placeholder="0.00">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Photo Ticket (Caméra en direct ou Fichier)</label>
              <input type="file" id="input-foto" class="form-control" accept="image/*" capture="environment">
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

  <!-- Modal Foto Ticket / Cámara -->
  <div class="modal fade" id="modalFoto" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-light">
          <h5 class="modal-title fw-bold"><i class="bi bi-camera text-dark me-2"></i>Photo du Ticket</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-center">
          <div id="foto-container" class="mb-3">
            <p class="text-muted small">Aucune photo enregistrée pour le moment.</p>
          </div>
          <div class="mb-3 text-start">
            <label class="form-label small fw-bold">Prendre une photo (Caméra) ou Choisir un fichier :</label>
            <input type="file" id="modal-input-foto" class="form-control form-control-sm" accept="image/*" capture="environment">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-light btn-sm fw-bold" data-bs-dismiss="modal">Fermer</button>
          <button type="button" class="btn btn-primary btn-sm fw-bold px-4" onclick="guardarFotoModal()">Enregistrer la photo</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Gestion Produits -->
  <div class="modal fade" id="modalProductos" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-light">
          <h5 class="modal-title fw-bold"><i class="bi bi-box-seam text-primary me-2"></i>Gestion des Produits Spécifiques</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <input type="hidden" id="edit-prod-index" value="-1">
          <div class="row g-2 mb-3 align-end bg-light p-3 rounded">
            <div class="col-md-4">
              <label class="form-label small fw-bold">Produit (ex: Viande, Fromage)</label>
              <input type="text" id="prod-nombre" class="form-control form-control-sm" placeholder="Nom">
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">Quantité</label>
              <input type="text" id="prod-cantidad" class="form-control form-control-sm" placeholder="Ex: 5 kg">
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">Prix Unitaire (€)</label>
              <input type="number" id="prod-precio" class="form-control form-control-sm" placeholder="0.00">
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button type="button" class="btn btn-success btn-sm w-100 fw-bold" id="btn-prod-accion" onclick="guardarProductoFila()">
                <i class="bi bi-plus-lg me-1"></i> Ajouter
              </button>
            </div>
          </div>
          
          <div class="table-responsive">
            <table class="table table-sm table-bordered align-middle mb-0" id="tabla-productos-detalle">
              <thead class="table-light">
                <tr>
                  <th>Produit</th>
                  <th>Quantité</th>
                  <th>Prix U</th>
                  <th class="text-center" style="width: 100px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- Contenido dinámico -->
              </tbody>
            </table>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary btn-sm fw-bold px-4" data-bs-dismiss="modal" onclick="actualizarDesgloseUI(activeRowForProducts)">Terminer</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Modificar Achat Principal -->
  <div class="modal fade" id="modalEditarAchat" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold"><i class="bi bi-pencil-square text-primary me-2"></i>Modifier l'Achat</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="form-editar">
            <div class="mb-3">
              <label class="form-label small fw-bold">Date d'achat</label>
              <input type="date" id="edit-date" class="form-control">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Provenance</label>
              <select id="edit-provenance" class="form-select">
                <option value="Cotsco">Cotsco</option>
                <option value="Fournisseur">Fournisseur</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-bold">Prix Total (€)</label>
              <input type="number" id="edit-precio" class="form-control">
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-light btn-sm fw-bold" data-bs-dismiss="modal">Annuler</button>
          <button type="button" class="btn btn-primary btn-sm fw-bold px-4" onclick="guardarEdicionAchat()"><i class="bi bi-check-lg me-1"></i> Mettre à jour</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    let activeRowForProducts = null;
    let activeRowForPhoto = null;
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

    function guardarRegistro() {
      const dateVal = document.getElementById('input-date').value;
      const prov = document.getElementById('input-provenance').value;
      const precio = parseFloat(document.getElementById('input-precio').value) || 0;
      const fotoInput = document.getElementById('input-foto');
      
      if(fotoInput.files && fotoInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          crearFilaConDatos(dateVal, prov, precio, e.target.result);
        };
        reader.readAsDataURL(fotoInput.files[0]);
      } else {
        crearFilaConDatos(dateVal, prov, precio, "");
      }
    }

    function crearFilaConDatos(dateVal, prov, precio, fotoBase64) {
      const provClass = prov === 'Cotsco' ? 'prov-cotsco' : 'prov-fournisseur';
      const tbody = document.querySelector('#tabla-achats tbody');
      
      const newMainRow = document.createElement('tr');
      newMainRow.setAttribute('data-productos', '[]');
      newMainRow.setAttribute('data-foto', fotoBase64);
      newMainRow.innerHTML = `
        <td class="fw-bold">${dateVal.split('-').reverse().join('/')}</td>
        <td><span class="prov-badge ${provClass}">${prov}</span></td>
        <td class="fw-bold text-primary">${precio.toFixed(2)} €</td>
        <td class="text-center">
          <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="abrirModalFoto(this)">
            <i class="bi bi-camera-fill text-dark me-1"></i> Photo
          </button>
        </td>
        <td class="text-center">
          <button class="btn btn-sm btn-outline-primary px-3 py-1 fw-bold" onclick="toggleDesglose(this)">
            <i class="bi bi-box-seam me-1"></i> Produits (<span class="prod-count">0</span>)
          </button>
        </td>
        <td class="text-center">
          <button class="btn btn-sm btn-light text-primary border-0" title="Modifier" onclick="abrirModalEditar(this)"><i class="bi bi-pencil-square"></i></button>
          <button class="btn btn-sm btn-light text-danger border-0" title="Supprimer" onclick="eliminarFila(this)"><i class="bi bi-trash-fill"></i></button>
        </td>
      `;

      tbody.insertBefore(newMainRow, tbody.firstChild);

      bootstrap.Modal.getInstance(document.getElementById('modalNouvelAchat')).hide();
      document.getElementById('form-achat').reset();
    }

    // FOTO / CÁMARA
    function abrirModalFoto(btn) {
      activeRowForPhoto = btn.closest('tr');
      const fotoData = activeRowForPhoto.getAttribute('data-foto');
      const container = document.getElementById('foto-container');
      
      if(fotoData) {
        container.innerHTML = `
          <img src="${fotoData}" class="img-fluid rounded mb-2" style="max-height: 200px;" alt="Ticket"><br>
          <a href="${fotoData}" download="ticket_achat.png" class="btn btn-sm btn-outline-success fw-bold"><i class="bi bi-download me-1"></i> Télécharger la photo</a>
        `;
      } else {
        container.innerHTML = `<p class="text-muted small">Aucune photo enregistrée pour le moment.</p>`;
      }
      document.getElementById('modal-input-foto').value = '';
      new bootstrap.Modal(document.getElementById('modalFoto')).show();
    }

    function guardarFotoModal() {
      if(!activeRowForPhoto) return;
      const fileInput = document.getElementById('modal-input-foto');
      if(fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          activeRowForPhoto.setAttribute('data-foto', e.target.result);
          bootstrap.Modal.getInstance(document.getElementById('modalFoto')).hide();
          alert("Photo enregistrée avec succès !");
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Veuillez prendre ou sélectionner une photo.");
      }
    }

    // TOGGLE DESGLOSE (Al pulsar el botón de productos se muestra/oculta abajo)
    function toggleDesglose(btn) {
      const mainRow = btn.closest('tr');
      activeRowForProducts = mainRow;
      const productos = JSON.parse(mainRow.getAttribute('data-productos') || '[]');

      let subRow = mainRow.nextElementSibling;
      const hasSubRow = subRow && subRow.classList.contains('subrow-tr');

      if (hasSubRow) {
        // Si ya está visible, lo cerramos/quitamos
        subRow.remove();
      } else {
        // Si no está visible, lo abrimos directamente o abrimos el modal si prefieres gestionar, pero aquí mostramos el desglose o abrimos modal. 
        // Vamos a hacer que al hacer clic abra directamente el modal para gestionar o ver:
        abrirModalProductos(btn);
      }
    }

    function abrirModalProductos(btn) {
      activeRowForProducts = btn.closest('tr');
      renderizarTablaProductosModal();
      new bootstrap.Modal(document.getElementById('modalProductos')).show();
    }

    function renderizarTablaProductosModal() {
      const productosJson = activeRowForProducts.getAttribute('data-productos') || '[]';
      const productos = JSON.parse(productosJson);
      const tbody = document.querySelector('#tabla-productos-detalle tbody');
      tbody.innerHTML = '';

      productos.forEach((p, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${p.nombre}</td>
          <td>${p.cantidad}</td>
          <td>${p.precio} €</td>
          <td class="text-center">
            <button type="button" class="btn btn-sm text-primary border-0 p-1" onclick="cargarProductoParaEditar(${index})" title="Modifier"><i class="bi bi-pencil-square"></i></button>
            <button type="button" class="btn btn-sm text-danger border-0 p-1" onclick="eliminarProductoFila(${index})" title="Supprimer"><i class="bi bi-trash-fill"></i></button>
          </td>
        `;
        tbody.appendChild(tr);
      });
      
      document.getElementById('edit-prod-index').value = "-1";
      document.getElementById('prod-nombre').value = "";
      document.getElementById('prod-cantidad').value = "";
      document.getElementById('prod-precio').value = "";
      document.getElementById('btn-prod-accion').innerHTML = '<i class="bi bi-plus-lg me-1"></i> Ajouter';
      document.getElementById('btn-prod-accion').className = "btn btn-success btn-sm w-100 fw-bold";
    }

    function guardarProductoFila() {
      if(!activeRowForProducts) return;
      const nombre = document.getElementById('prod-nombre').value;
      const cantidad = document.getElementById('prod-cantidad').value;
      const precio = document.getElementById('prod-precio').value;
      const editIndex = parseInt(document.getElementById('edit-prod-index').value);

      if(!nombre) {
        alert("Veuillez saisir le nom du produit.");
        return;
      }

      let productos = JSON.parse(activeRowForProducts.getAttribute('data-productos') || '[]');

      if(editIndex === -1) {
        productos.push({nombre, cantidad, precio});
      } else {
        productos[editIndex] = {nombre, cantidad, precio};
      }

      activeRowForProducts.setAttribute('data-productos', JSON.stringify(productos));
      activeRowForProducts.querySelector('.prod-count').innerText = productos.length;
      actualizarDesgloseUI(activeRowForProducts);
      renderizarTablaProductosModal();
    }

    function cargarProductoParaEditar(index) {
      let productos = JSON.parse(activeRowForProducts.getAttribute('data-productos') || '[]');
      const p = productos[index];
      
      document.getElementById('prod-nombre').value = p.nombre;
      document.getElementById('prod-cantidad').value = p.cantidad;
      document.getElementById('prod-precio').value = p.precio;
      document.getElementById('edit-prod-index').value = index;

      document.getElementById('btn-prod-accion').innerHTML = '<i class="bi bi-check-lg me-1"></i> Mettre à jour';
      document.getElementById('btn-prod-accion').className = "btn btn-primary btn-sm w-100 fw-bold";
    }

    function eliminarProductoFila(index) {
      if(!activeRowForProducts) return;
      let productos = JSON.parse(activeRowForProducts.getAttribute('data-productos') || '[]');
      productos.splice(index, 1);
      
      activeRowForProducts.setAttribute('data-productos', JSON.stringify(productos));
      activeRowForProducts.querySelector('.prod-count').innerText = productos.length;
      actualizarDesgloseUI(activeRowForProducts);
      renderizarTablaProductosModal();
    }

    function actualizarDesgloseUI(mainRow) {
      const productos = JSON.parse(mainRow.getAttribute('data-productos') || '[]');
      let subRow = mainRow.nextElementSibling;
      const hasSubRow = subRow && subRow.classList.contains('subrow-tr');

      if (productos.length === 0) {
        if (hasSubRow) subRow.remove();
      } else {
        const htmlContent = `
          <td colspan="6" class="p-0">
            <div class="subrow-container">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="fw-bold text-secondary small"><i class="bi bi-arrowreturn-right me-1"></i> Produits associés :</span>
                <button class="btn btn-sm btn-link text-danger p-0 small text-decoration-none" onclick="cerrarDesglose(this)"><i class="bi bi-x-circle me-1"></i> Fermer le desglose</button>
              </div>
              <ul class="mb-0 ps-3 small text-muted lista-desglose">
                ${productos.map(p => `<li><strong>${p.nombre}</strong> - Quantité: ${p.cantidad} - Prix U: ${p.precio} €</li>`).join('')}
              </ul>
            </div>
          </td>
        `;
        if (hasSubRow) {
          subRow.innerHTML = htmlContent;
        } else {
          subRow = document.createElement('tr');
          subRow.className = 'table-light subrow-tr';
          subRow.innerHTML = htmlContent;
          mainRow.parentNode.insertBefore(subRow, mainRow.nextSibling);
        }
      }
    }

    function cerrarDesglose(btn) {
      const subRow = btn.closest('tr');
      if(subRow) subRow.remove();
    }

    // MODIFICAR COMPRA PRINCIPAL
    function abrirModalEditar(btn) {
      currentRowToEdit = btn.closest('tr');
      const datePart = currentRowToEdit.cells[0].innerText.split('/');
      const isoDate = `${datePart[2]}-${datePart[1]}-${datePart[0]}`;
      const provText = currentRowToEdit.cells[1].querySelector('.prov-badge').innerText.trim();
      const precioVal = parseFloat(currentRowToEdit.cells[2].innerText) || 0;

      document.getElementById('edit-date').value = isoDate;
      document.getElementById('edit-provenance').value = provText;
      document.getElementById('edit-precio').value = precioVal;

      new bootstrap.Modal(document.getElementById('modalEditarAchat')).show();
    }

    function guardarEdicionAchat() {
      if (!currentRowToEdit) return;

      const dateVal = document.getElementById('edit-date').value;
      const prov = document.getElementById('edit-provenance').value;
      const precio = parseFloat(document.getElementById('edit-precio').value) || 0;
      const provClass = prov === 'Cotsco' ? 'prov-cotsco' : 'prov-fournisseur';

      currentRowToEdit.cells[0].innerText = dateVal.split('-').reverse().join('/');
      currentRowToEdit.cells[1].innerHTML = `<span class="prov-badge ${provClass}">${prov}</span>`;
      currentRowToEdit.cells[2].innerText = precio.toFixed(2) + ' €';

      bootstrap.Modal.getInstance(document.getElementById('modalEditarAchat')).hide();
    }

    function eliminarFila(btn) {
      if(confirm("Voulez-vous vraiment supprimer cet achat ?")) {
        const mainRow = btn.closest('tr');
        const subRow = mainRow.nextElementSibling;
        if(subRow && subRow.classList.contains('subrow-tr')) subRow.remove();
        mainRow.remove();
      }
    }
  </script>

</body>
</html>
"""

components.html(html_achats, height=1300, scrolling=False)