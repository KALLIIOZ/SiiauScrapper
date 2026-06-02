import json
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
DEFAULT_TELEGRAM_CHAT_IDS = [
    int(chat_id.strip())
    for chat_id in os.getenv("TELEGRAM_CHAT_IDS", "").split(",")
    if chat_id.strip()
]
SIIAU_CODIGO = os.getenv("SIIAU_CODIGO", "").strip()
SIIAU_NIP = os.getenv("SIIAU_NIP", "").strip()
SIIAU_CICLO = os.getenv("SIIAU_CICLO", "").strip()
MONITORING_CONFIG_PATH = Path(os.getenv("MONITORING_CONFIG_PATH", PROJECT_ROOT / "monitoring_config.json"))
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "5"))
LOG_FILE = os.getenv("LOG_FILE", "errores.log").strip()

if not TELEGRAM_BOT_TOKEN:
    raise EnvironmentError(
        "Debe configurar TELEGRAM_BOT_TOKEN en el archivo .env o en las variables de entorno."
    )

if not MONITORING_CONFIG_PATH.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo de configuración de monitorización: {MONITORING_CONFIG_PATH}"
    )

with open(MONITORING_CONFIG_PATH, encoding="utf-8") as config_file:
    try:
        MONITORING_CONFIG = json.load(config_file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"monitoring_config.json no es un JSON válido: {exc}"
        ) from exc

if "monitors" not in MONITORING_CONFIG or not isinstance(MONITORING_CONFIG["monitors"], list):
    raise ValueError(
        "monitoring_config.json debe definir un array 'monitors' con cada monitor y sus URLs."
    )
