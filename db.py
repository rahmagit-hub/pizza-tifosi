import pandas as pd
from pathlib import Path

EXCEL_PATH = Path(__file__).parent / "tifosi_data.xlsx"
ROYALTY = 0.03

def init_db():
    """Crea el archivo Excel con todas las hojas necesarias si no existe."""
    if not EXCEL_PATH.exists():
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
            pd.DataFrame(columns=["id", "fecha", "especes", "carte", "livraison", "reserve"]).to_excel(writer, sheet_name="ventes", index=False)
            pd.DataFrame(columns=["id", "fecha", "provenance", "prix_total"]).to_excel(writer, sheet_name="achats", index=False)
            pd.DataFrame(columns=["id", "nom", "stock", "prix"]).to_excel(writer, sheet_name="inventaire", index=False)
            pd.DataFrame(columns=["id", "nom", "poste", "salaire"]).to_excel(writer, sheet_name="personnel", index=False)
            pd.DataFrame(columns=["id", "mois", "categorie", "montant"]).to_excel(writer, sheet_name="charges", index=False)

# --- VENTES ---
def add_vente(fecha, especes, carte, livraison, reserve):
    init_db()
    df = pd.read_excel(EXCEL_PATH, sheet_name="ventes")
    new_id = int(df["id"].max() + 1) if not df.empty and "id" in df.columns and pd.notna(df["id"].max()) else 1
    nueva_fila = pd.DataFrame([{"id": new_id, "fecha": str(fecha), "especes": float(especes), "carte": float(carte), "livraison": float(livraison), "reserve": int(reserve)}])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="ventes", index=False)

def get_ventes():
    init_db()
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="ventes")
        if df.empty or "fecha" not in df.columns:
            return pd.DataFrame(columns=["id", "fecha", "especes", "carte", "livraison", "reserve", "total", "redevance"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        df["reserve"] = df["reserve"].astype(bool)
        df["total"] = df["especes"].fillna(0) + df["carte"].fillna(0) + df["livraison"].fillna(0)
        df["redevance"] = df["total"] * ROYALTY
        return df.sort_values(by="fecha", ascending=False)
    except Exception:
        return pd.DataFrame(columns=["id", "fecha", "especes", "carte", "livraison", "reserve", "total", "redevance"])

# --- ACHATS ---
def add_achat(fecha, provenance, prix_total):
    init_db()
    df = pd.read_excel(EXCEL_PATH, sheet_name="achats")
    new_id = int(df["id"].max() + 1) if not df.empty and "id" in df.columns and pd.notna(df["id"].max()) else 1
    nueva_fila = pd.DataFrame([{"id": new_id, "fecha": str(fecha), "provenance": provenance, "prix_total": float(prix_total)}])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="achats", index=False)

def get_achats():
    init_db()
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="achats")
        return df if not df.empty else pd.DataFrame(columns=["id", "fecha", "provenance", "prix_total"])
    except Exception:
        return pd.DataFrame(columns=["id", "fecha", "provenance", "prix_total"])

# --- INVENTAIRE ---
def save_inventaire(df_data):
    init_db()
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_data.to_excel(writer, sheet_name="inventaire", index=False)

def get_inventaire():
    init_db()
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="inventaire")
        return df if not df.empty else pd.DataFrame(columns=["id", "nom", "stock", "prix"])
    except Exception:
        return pd.DataFrame(columns=["id", "nom", "stock", "prix"])

# --- PERSONNEL ---
def add_personnel(nom, poste, salaire):
    init_db()
    df = pd.read_excel(EXCEL_PATH, sheet_name="personnel")
    new_id = int(df["id"].max() + 1) if not df.empty and "id" in df.columns and pd.notna(df["id"].max()) else 1
    nueva_fila = pd.DataFrame([{"id": new_id, "nom": nom, "poste": poste, "salaire": float(salaire)}])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="personnel", index=False)

def get_personnel():
    init_db()
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="personnel")
        return df if not df.empty else pd.DataFrame(columns=["id", "nom", "poste", "salaire"])
    except Exception:
        return pd.DataFrame(columns=["id", "nom", "poste", "salaire"])

# --- CHARGES FIXES ---
def add_charge(mois, categorie, montant):
    init_db()
    df = pd.read_excel(EXCEL_PATH, sheet_name="charges")
    new_id = int(df["id"].max() + 1) if not df.empty and "id" in df.columns and pd.notna(df["id"].max()) else 1
    nueva_fila = pd.DataFrame([{"id": new_id, "mois": mois, "categorie": categorie, "montant": float(montant)}])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="charges", index=False)

def get_charges():
    init_db()
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="charges")
        return df if not df.empty else pd.DataFrame(columns=["id", "mois", "categorie", "montant"])
    except Exception:
        return pd.DataFrame(columns=["id", "mois", "categorie", "montant"])