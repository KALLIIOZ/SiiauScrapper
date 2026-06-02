# Instrucciones de Refactorización para Copilot

## Contexto del Proyecto
Este repositorio contiene un web scraper en Python (`SiiauScrapper`) diseñado para monitorear la disponibilidad de cupos en un sistema universitario (SIIAU) y notificar a los usuarios a través de Telegram. 

Actualmente, el proyecto cumple su función pero requiere una refactorización profunda para adoptar prácticas de desarrollo backend profesional. El objetivo es estructurar el código pensando en una arquitectura limpia y modular, preparándolo para una posible evolución hacia un entorno de microservicios o una arquitectura orientada a eventos.

## Archivos Actuales a Analizar
Por favor, analiza el estado actual de los siguientes archivos antes de proponer cambios:
- `AutomationFail.py`
- `TelegramConsult.py`
- `TelgramConsultIvan.py`
- `telegramconsult2.py`
- `TerminalConsult.py`
- `requirements.txt`

## Tareas de Refactorización (Ejecutar paso a paso)

### Paso 1: Seguridad y Configuración (Variables de Entorno)
1. Extrae todas las credenciales "hardcodeadas" del código fuente, como `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, y variables como el código de estudiante (`codigo`) y el NIP en `AutomationFail.py`.
2. Implementa la carga de estas variables utilizando la librería `python-dotenv`.
3. Genera un archivo `.env.example` que documente las variables requeridas sin exponer datos reales.

### Paso 2: Unificación de Scripts (Principio DRY)
Actualmente existen múltiples archivos redundantes (`TelegramConsult.py`, `TelgramConsultIvan.py`, `telegramconsult2.py`, `TerminalConsult.py`) que hacen prácticamente lo mismo con ligeras variaciones de usuarios y materias.
1. Crea un único archivo principal (ej. `main.py`).
2. Diseña un sistema de configuración basado en un diccionario o archivo JSON/YAML donde se definan los `chat_id` y las listas de URLs (o NRCs) que cada usuario desea monitorear.
3. El script principal debe iterar sobre esta configuración, evitando la duplicación de lógica.

### Paso 3: Robustez en la Extracción de Datos (Scraping)
La lógica actual utiliza una lista plana y saltos de índice rígidos (`j += 8`) para parsear el HTML, lo cual es altamente frágil ante cambios en la UI de la página objetivo.
1. Refactoriza la extracción con `BeautifulSoup` para iterar directamente sobre las filas de la tabla (`<tr>`).
2. Extrae los datos accediendo a las celdas individuales (`<td>`) de cada fila (ej. índice 0 para NRC, índice 2 para Materia, etc.).
3. Devuelve los datos estructurados en una lista de diccionarios o `dataclasses` (ej. `[{'nrc': 12345, 'materia': 'Ejemplo', 'cupo': 3}]`).

### Paso 4: Portabilidad y Gestión de Certificados SSL
En archivos como `AutomationFail.py`, las peticiones a la API utilizan rutas absolutas de Windows para la validación de certificados (`verify=r"C:\Users\aponc\Downloads\siiau.crt"`).
1. Modifica la gestión de certificados para que el código sea agnóstico al sistema operativo y fácilmente "dockerizable" para despliegues en la nube.
2. Utiliza rutas relativas (ej. guardando el certificado en una carpeta `certs/` en el repo) o configura las peticiones para que utilicen los certificados del sistema de forma segura.

### Paso 5: Arquitectura Modular (Separación de Responsabilidades)
Reestructura el bucle principal infinito (`while True`) separando el código en módulos distintos y cohesivos:
1. **Fetcher / Parser:** Un módulo dedicado exclusivamente a realizar la petición HTTP y devolver datos limpios.
2. **Evaluador (Business Logic):** Un módulo que reciba los datos limpios y evalúe las reglas de disponibilidad (ej. determinar si la alerta es "Baja Disponibilidad" o "Crítica").
3. **Notifier:** Un módulo encargado únicamente de formatear y enviar el mensaje a la API de Telegram.

### Paso 6: Actualización de Dependencias
Asegúrate de actualizar el archivo `requirements.txt` para incluir únicamente las librerías que finalmente se utilicen en esta nueva versión (por ejemplo, añadiendo `python-dotenv` y removiendo `python-telegram-bot` del README si se opta por seguir usando llamadas directas con `requests`).

---
**Instrucción Final para Copilot:** No generes todo el código de una sola vez. Pregúntame por cuál de estos 6 pasos quiero empezar, y vayamos refactorizando el proyecto de forma iterativa, explicando brevemente los beneficios de escalabilidad en cada cambio.