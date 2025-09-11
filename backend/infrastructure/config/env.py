import os
from dotenv import load_dotenv
from pathlib import Path

# Charge en priorité djouman/settings/.env si présent
ROOT = Path(__file__).resolve().parents[3]
candidate = ROOT / "djouman" / "settings" / ".env"
if candidate.exists():
    load_dotenv(candidate)
else:
    load_dotenv()  # fallback: .env à la racine si dispo
