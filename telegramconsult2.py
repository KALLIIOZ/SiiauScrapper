import requests
from bs4 import BeautifulSoup as b
import os
import time
from colorama import Fore, init

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

# Lista de URLs de materias
urls = [
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL358",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL357",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL370",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL372",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL359",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL368",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL385",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL375",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL373",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL381",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202520&cup=D&crsep=IL378",
]

# Estado previo de los cupos
estado_previo = {}

while True:
    try:
        for url in urls:
            try:
                html = requests.get(url, timeout=10)  # timeout para evitar que se congele
                html.raise_for_status()  # lanza error si el código no es 200
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"Error al conectar con {url}: {e}")
                continue  # salta a la siguiente URL

            content = html.content
            soup = b(content, "html.parser")

            lst = []
            lstNRC = []
            lstCupo = []
            lstMateria = []
            lstProfe = []

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

                # Compara con el estado previo
                if nrc not in estado_previo or cupo_actual != estado_previo[nrc]:
                    estado_previo[nrc] = cupo_actual  # Actualiza el estado previo

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

        time.sleep(1)  # Espera antes de la siguiente consulta
        os.system('cls')

    except Exception as e:
        print(Fore.RED + f"\n[ERROR CRÍTICO] {e}")
        print(Fore.YELLOW + "Reiniciando el script en 5 segundos...\n")
        time.sleep(5)
