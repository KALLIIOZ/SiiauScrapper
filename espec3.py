import requests
from bs4 import BeautifulSoup as b
import os
import time
from colorama import Fore, init
import re

init()

# Token del bot y chat ID de Telegram
TELEGRAM_BOT_TOKEN = "7829332726:AAGC45zHCahGmymy_4T00_5wok8YpZLsg2w"
TELEGRAM_CHAT_ID = "6107130195"

def send_telegram_message(message):
    """Función para enviar un mensaje por Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + "Mensaje enviado por Telegram.")
        else:
            print(Fore.RED + "Error al enviar el mensaje por Telegram.")
    except Exception as e:
        print(Fore.RED + f"Excepción al enviar mensaje: {e}")

def obtener_pidmp(codigo, NIP):
    """Obtiene el valor de pidmp haciendo una solicitud similar al comando cURL."""
    url = "https://siiauescolar.siiau.udg.mx/wus/GUPPRINCIPAL.VALIDA_INICIO"
    headers = {
        "Origin": "https://siiauescolar.siiau.udg.mx",
        "Referer": "https://siiauescolar.siiau.udg.mx/wus/gupprincipal.forma_inicio_bd",
    }
    data = {
        "p_codigo_c": codigo,
        "p_clave_c": NIP,
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=15, verify=r"C:\Users\aponc\Downloads\siiau.crt")
        if response.status_code == 200:
            match = re.search(r'VALUE="(.*?)">', response.text)
            if match:
                print(match.group(1))
                return match.group(1)  # Retornar el valor encontrado
            else:
                print(Fore.RED + "No se encontró el valor de pidmp en la respuesta.")
                return None
        else:
            print(Fore.RED + f"Error en la solicitud para obtener pidmp: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(Fore.RED + f"Excepción al obtener pidmp: {e}")
        return None

def obtener_ifcarrera(cookies, pidmp, carreras):
    """Obtiene el valor correcto de `ifcarrera` basado en la lógica."""
    headers = {
        "Referer": f"http://siiauescolar.siiau.udg.mx/wal/gupmenug.menu?p_sistema_c=ALUMNOS&p_sistemaid_n=3&p_menupredid_n=3&p_pidm_n={pidmp}&p_majr_c={pidmp}",
    }

    if not carreras:
        url = f"http://siiauescolar.siiau.udg.mx/wal/gupmenug.menu?p_sistema_c=ALUMNOS&p_sistemaid_n=3&p_menupredid_n=3&p_pidm_n={pidmp}&p_majr_c={pidmp}"
        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=15, verify=r"C:\Users\aponc\Downloads\siiau.crt")
            if response.status_code == 200:
                match = re.search(r'majrp=(.*?)" target', response.text)
                if match:
                    return match.group(1)
        except requests.RequestException as e:
            print(f"Error al consultar ifcarrera: {e}")
            return None
    else:
        for line in carreras:
            url = f"https://siiauescolar.siiau.udg.mx/wal/sfpregw.inicio?pidmp={pidmp}&majrp={line}"
            try:
                response = requests.get(url, headers=headers, cookies=cookies, timeout=15, verify=r"C:\Users\aponc\Downloads\siiau.crt")
                if response.status_code == 200 and "<TITLE>Registro" in response.text:
                    return line
            except requests.RequestException as e:
                print(f"Error al consultar carrera {line}: {e}")
                continue

    return None

def registrar_materia(codigo, pidmp, ciclo, ifcarrera, cup, NRC):
    """Automatiza el registro de una materia en SIIAU."""
    cookies = {"cookies": f"{NRC}{codigo}"}
    url = "https://siiauescolar.siiau.udg.mx/wal/sfpregw.procesa_registro"
    headers = {
        "Origin": "http://siiauescolar.siiau.udg.mx",
        "Referer": f"http://siiauescolar.siiau.udg.mx/wal/sfpregw.inicio?pidmp={pidmp}&majrp={ifcarrera}",
    }
    data = {
        "pidmp": pidmp,
        "ciclop": ciclo,
        "majrp": ifcarrera,
        "levlp": "",
        "cup": cup,
        "collp": "",
        "crnp": NRC,
        **{f"crnp{n}": "" for n in range(1, 9)},
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            cookies=cookies,
            data=data,
            timeout=15,
            verify=r"C:\Users\aponc\Downloads\_.siiau.udg.mx.crt",
        )
        if response.status_code == 200:
            return response.text
        else:
            return f"Error en el registro: {response.status_code}"
    except requests.RequestException as e:
        return f"Excepción al registrar materia: {e}"

# Configuración inicial
codigo = "218797828"  # Tu código de estudiante
NIP = "fortaleza2"      # Tu clave NIP
ciclo = "202510"
pidmp = obtener_pidmp(codigo, NIP)
if not pidmp:
    print(Fore.RED + "No se pudo obtener el pidmp. Verifica tus credenciales.")
    exit()

# Lista de URLs de materias
urls = [
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=CB224",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL367",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL358",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL364",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL369",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL357",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL366"
]
# Bucle principal
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
            if lstCupo[x] > 0:
                mensaje = (
                    f"🎓 *Materia Disponible:*\n"
                    f"📘 Materia: {lstMateria[0] if lstMateria else 'Desconocida'}\n"
                    f"👨‍🏫 Profesor: {lstProfe[x]}\n"
                    f"📌 NRC: {lstNRC[x]}\n"
                    f"✅ Cupos Disponibles: {lstCupo[x]}"
                )
                send_telegram_message(mensaje)

                ifcarrera = obtener_ifcarrera({"cookies": f"{lstNRC[x]}{codigo}"}, pidmp, [])
                if ifcarrera:
                    registro = registrar_materia(codigo, pidmp, ciclo, ifcarrera, lstCupo[x], lstNRC[x])
                    print(f"Resultado del registro: {registro}")

    time.sleep(10)
    os.system('cls')


