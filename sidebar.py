import streamlit as st

def render_sidebar():
    st.markdown("""
        <style>
        /* Ocultar elementos nativos */
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        
        /* Fondo blanco puro y sin padding excesivo arriba */
        section[data-testid="stSidebar"] { 
            background-color: #ffffff !important; 
            border-right: 2px solid #e9ecef !important;
            padding: 4px 2rem 2rem 2rem !important;
            width: 300px !important;
        }
        
        /* Forzar subida absoluta del bloque superior */
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 1.5em !important;
        }
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0px !important;
            margin-top: -50px !important;
        }
        
        /* Nombre PIZZA_TIFOSI Repentigny muy arriba, verde grande y limpio */
        .sidebar-title { 
            font-size: 2.4rem !important; 
            font-weight: 800 !important; 
            color: #15803d !important; 
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            letter-spacing: -0.5px;
        }
        .sidebar-subtitle {
            font-size: 0.8rem !important;
            color: #64748b !important;
            margin-bottom: 0.8rem !important;
        }

        /* Cada pestaña como tarjeta flotante con sombra negra tipo 3D */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] { 
            background-color: #ffffff !important;
            border-radius: 10px !important; 
            padding: 0.7rem 1rem !important; 
            margin-bottom: 0.6rem !important;
            border: 1px solid #f1f5f9 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.2s ease-in-out;
        }
        
        /* Texto e iconos de las pestañas */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] span {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
        }

        /* Efecto Hover en las pestañas */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover { 
            background-color: #f8fafc !important;
            box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.12), 0 3px 6px -1px rgba(0, 0, 0, 0.06) !important;
            transform: translateY(-1px);
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover span { 
            color: #15803d !important; 
        }

        /* Pestaña activa seleccionada */
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
            background-color: #15803d !important;
            box-shadow: 0 4px 8px rgba(21, 128, 61, 0.3) !important;
        }
        [data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] span {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🍕 PIZZA TIFOSI</div>', unsafe_allow_html=True)
        
        st.page_link("app.py", label="Tableau de Bord", icon="📊")
        st.page_link("pages/1_Ventes.py", label="Ventes / Caisse", icon="🛒")
        st.page_link("pages/2_Achats.py", label="Achats", icon="🛍️")
        st.page_link("pages/3_Inventaire.py", label="Inventaire & Stocks", icon="📦")
        st.page_link("pages/4_Personnel.py", label="Personnel & Paie", icon="👥")
        st.page_link("pages/5_Charges.py", label="Charges Fixes", icon="🧾")
        
        st.markdown("<hr style='margin: 0.8rem 0; border-color: #e9ecef;'>", unsafe_allow_html=True)
        st.caption("🌐 Sync ES / CA")