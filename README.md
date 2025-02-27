# Web Scraper para Página Escolar con Notificaciones en Telegram

Este repositorio contiene un script diseñado para **scrapear información de una página web escolar** y **enviar notificaciones a través de Telegram** cuando se detectan cambios o actualizaciones.

## 🚀 Características

- Extrae información relevante de una página web escolar (por ejemplo, noticias, calificaciones, eventos, etc.).
- Detecta cambios en el contenido de la página.
- Envía notificaciones en tiempo real a un chat de Telegram utilizando el bot de Telegram.
- Configuración sencilla para personalizar la URL de la página y el contenido a monitorear.

## 📦 Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes paquetes de Python:

- `requests`: Para hacer solicitudes HTTP a la página web.
- `BeautifulSoup4`: Para analizar y extraer datos HTML.
- `python-telegram-bot`: Para enviar notificaciones en Telegram.

Puedes instalarlos usando:

pip install requests beautifulsoup4 python-telegram-bot

## ⚙️ Configuración
Crear un bot de Telegram

Ve a BotFather en Telegram y crea un nuevo bot.
Obtén el Token del bot que te proporcionará BotFather.
Obtener tu ID de Chat

Abre una conversación con tu bot y envíale cualquier mensaje.
Usa una herramienta como GetIDs para obtener tu Chat ID.
Configura tus credenciales en el código
En el archivo de configuración o directamente en el script, agrega:

python
Copiar
Editar
TELEGRAM_BOT_TOKEN = 'TU_TOKEN_DEL_BOT'
TELEGRAM_CHAT_ID = 'TU_CHAT_ID'
URL_OBJETIVO = 'URL_DE_LA_PAGINA_ESCOLAR'

##▶️ Uso
Ejecuta el script usando:

bash
Copiar
Editar
python nombre_del_script.py
El scraper verificará la página web y enviará una notificación a tu Telegram si detecta cambios en el contenido monitoreado.

##⚠️ Advertencias y Limitaciones
Respeta las políticas de uso del sitio web: Antes de hacer scraping, asegúrate de cumplir con los Términos de Servicio del sitio web escolar.
No sobrecargues el servidor: Configura tiempos de espera adecuados entre solicitudes para no causar una carga excesiva en el servidor web.
Este proyecto es solo para fines educativos. No uses este script para actividades malintencionadas o que violen las leyes locales.
##🤝 Contribuciones
Si deseas mejorar este proyecto, ¡eres bienvenido! Abre un Issue o envía un Pull Request con tus sugerencias o mejoras.
