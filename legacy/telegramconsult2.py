import requests
from bs4 import BeautifulSoup as b
import os, random
import time
from colorama import Fore, init
from datetime import datetime
import traceback

init()

# Token del bot y chat ID de Telegram
TELEGRAM_BOT_TOKEN = "7829332726:AAGC45zHCahGmymy_4T00_5wok8YpZLsg2w"
TELEGRAM_CHAT_ID = ["6107130195"]  # "7759974191" es ivan

def send_telegram_message(message):
    """Función para enviar un mensaje por Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    for chat_id in TELEGRAM_CHAT_ID:
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + "Mensaje enviado por Telegram.")
            else:
                print(Fore.RED + f"Error al enviar mensaje por Telegram: {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"Excepción al enviar mensaje: {e}")

def registrar_error(error, url=None, enviar_telegram=False):
    """Registra errores en un archivo con fecha, hora, URL y stacktrace.
       Opcionalmente envía el error por Telegram."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    traza = traceback.format_exc()

    log_text = f"\n[{fecha}]\n"
    if url:
        log_text += f"URL: {url}\n"
    log_text += f"Error: {error}\n"
    log_text += "Stacktrace:\n" + traza + "\n" + "="*80 + "\n"

    with open("errores.log", "a", encoding="utf-8") as f:
        f.write(log_text)

    if enviar_telegram:
        try:
            send_telegram_message(f"🚨 *Error Detectado*\nFecha: {fecha}\nURL: {url or 'N/A'}\nError: {error}")
        except:
            pass  # Evita que un fallo en el envío interrumpa el script

# Lista de URLs de materias
urls = [
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL357",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL370",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL372",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL359",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL368",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL375",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL373",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL378",
]

# Estado previo de los cupos
estado_previo = {}

while True:
    try:
        for url in urls:
            try:
                html = requests.get(url, timeout=10)
                html.raise_for_status()
            except requests.exceptions.RequestException as e:
                registrar_error("Error al conectar", url, enviar_telegram=True)
                print(Fore.RED + f"Error al conectar con {url}: {e}")
                continue

            try:
                content = html.content
                soup = b(content, "html.parser")

                lst, lstNRC, lstCupo, lstMateria, lstProfe = [], [], [], [], []

                materia = soup.find_all('td', class_='tddatos')
                for i in materia:
                    lst.append(i.text.strip())

                j = 0
                while j < len(lst):
                    lstNRC.append(lst[j])
                    j += 8

                j = 2
                while j < len(lst):
                    lstMateria.append(lst[j])
                    j += 8

                j = 7
                while j < len(lst):
                    profesor = lst[j].strip().replace("01", "").strip()
                    lstProfe.append(profesor)
                    j += 8

                j = 6
                while j < len(lst):
                    lstCupo.append(lst[j])
                    j += 8

                lstNRC = list(map(int, lstNRC))
                lstCupo = list(map(int, lstCupo))

                for x in range(len(lstCupo)):
                    nrc = lstNRC[x]
                    cupo_actual = lstCupo[x]

                    if nrc not in estado_previo or cupo_actual != estado_previo[nrc]:
                        estado_previo[nrc] = cupo_actual

                        if 1 < cupo_actual <= 5:
                            mensaje = (
                                f"⚠️ *¡Alerta de Baja Disponibilidad!*\n"
                                f"📘 Materia: {lstMateria[0] if lstMateria else 'Desconocida'}\n"
                                f"👨‍🏫 Profesor: {lstProfe[x]}\n"
                                f"📌 NRC: {lstNRC[x]}\n"
                                f"✅ Cupos Disponibles: {lstCupo[x]}"
                            )
                            send_telegram_message(mensaje)
                        elif cupo_actual == 1:
                            mensaje = (
                                f"🚨 *¡Alerta Crítica de Disponibilidad!*\n"
                                f"📘 Materia: {lstMateria[0] if lstMateria else 'Desconocida'}\n"
                                f"👨‍🏫 Profesor: {lstProfe[x]}\n"
                                f"📌 NRC: {lstNRC[x]}\n"
                                f"✅ Cupos Disponibles: {lstCupo[x]}"
                            )
                            send_telegram_message(mensaje)
                        elif 5 < cupo_actual < 15:
                            mensaje = (
                                f"🎓 *Materia Disponible:*\n"
                                f"📘 Materia: {lstMateria[0] if lstMateria else 'Desconocida'}\n"
                                f"👨‍🏫 Profesor: {lstProfe[x]}\n"
                                f"📌 NRC: {lstNRC[x]}\n"
                                f"✅ Cupos Disponibles: {lstCupo[x]}"
                            )
                            send_telegram_message(mensaje)

            except Exception as e:
                registrar_error("Error procesando datos", url, enviar_telegram=True)
                print(Fore.RED + f"Error procesando datos de {url}: {e}")

        time.sleep(random.uniform(2, 8))
        os.system('cls')

    except Exception as e:
        registrar_error(f"[ERROR CRÍTICO] {e}", enviar_telegram=True)
        print(Fore.RED + f"\n[ERROR CRÍTICO] {e}")
        print(Fore.YELLOW + "Reiniciando el script en 5 segundos...\n")
        time.sleep(5)
