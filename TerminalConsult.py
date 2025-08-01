import requests
from bs4 import BeautifulSoup as b
import os
import time
from colorama import Fore, init

init()

# Token del bot y chat ID de Telegram
TELEGRAM_BOT_TOKEN = "7829332726:AAGC45zHCahGmymy_4T00_5wok8YpZLsg2w"
TELEGRAM_CHAT_ID = ["6107130195","7759974191"]

def send_telegram_message(message):
    """Función para enviar un mensaje por Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    for chat_id in TELEGRAM_CHAT_ID:
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(Fore.GREEN + "Mensaje enviado por Telegram.")
            else:
                print(Fore.RED + "Error al enviar el mensaje por Telegram.")
        except Exception as e:
            print(Fore.RED + f"Excepción al enviar mensaje: {e}")

# Lista de URLs de materias
urls = [
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL384",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL375",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=CB224",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL367",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL358",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL364",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL369",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL357",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL366",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL370",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL381"
]


while True:
    for url in urls:
        html = requests.get(url)
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
            if lstCupo[x] > 0:  # Si hay cupos disponibles
                mensaje = (
                    f"🎓 *Materia Disponible:*\n"
                    f"📘 Materia: {lstMateria[0] if lstMateria else 'Desconocida'}\n"
                    f"👨‍🏫 Profesor: {lstProfe[x]}\n"
                    f"📌 NRC: {lstNRC[x]}\n"
                    f"✅ Cupos Disponibles: {lstCupo[x]}"
                )
                send_telegram_message(mensaje)
    time.sleep(5)
    os.system('cls')
