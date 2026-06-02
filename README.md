# Web Scraper para Página Escolar con Notificaciones en Telegram

Este repositorio contiene un scraper modular para monitorear la disponibilidad de cupos en SIIAU y enviar alertas por Telegram.

## 🚀 Arquitectura

- `main.py`: controlador principal que orquesta la lectura de configuración, el scraping y el envío de alertas.
- `fetcher.py`: extrae datos HTML y devuelve cursos estructurados.
- `evaluator.py`: aplica la lógica de disponibilidad y construye el texto de la alerta.
- `notifier.py`: envía mensajes a Telegram usando la API de `requests`.
- `settings.py`: carga variables sensibles desde `.env` y valida la configuración.

## 📦 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

Las dependencias son:

- `requests`
- `beautifulsoup4`
- `python-dotenv`

## ⚙️ Configuración

1. Copia `.env.example` a `.env`.
2. Ajusta `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_IDS`.
3. Modifica `monitoring_config.json` para definir los monitores, `chat_ids` y `urls`.

### Ejemplo de `.env`

```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
TELEGRAM_CHAT_IDS=6107130195,7759974191
POLL_INTERVAL_SECONDS=5
MONITORING_CONFIG_PATH=monitoring_config.json
LOG_FILE=errores.log
```

## ▶️ Uso

Ejecuta el monitoreo con:

```bash
python main.py
```

El script consultará los URLs configurados y enviará alertas si cambia la disponibilidad de cupos.

## 📌 Notas

- La configuración principal de los monitores está en `monitoring_config.json`.
- La lógica de scraping ya no depende de saltos rígidos en la tabla HTML; usa filas y celdas.
- Las credenciales sensibles se cargan desde `.env`, lo que facilita despliegues y mantiene el código limpio.

## 🤝 Contribuciones
Si deseas mejorar este proyecto, abre un Issue o envía un Pull Request con tus sugerencias.
