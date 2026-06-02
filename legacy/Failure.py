import requests
from bs4 import BeautifulSoup as b
import os
import time
from colorama import Fore, init

init()

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
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL361",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL372",
    "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop=202510&cup=D&crsep=IL381"
]

# Ciclo principal
while True:
    os.system('cls')
    for url in urls:
        html = requests.get(url)
        content = html.content
        soup = b(content, "html.parser")

        # Listas para almacenar los datos
        lst = []
        lstNRC = []
        lstCupo = []
        lstMateria = []
        lstProfe = []

        # Extraer la información de materia y profesor
        materia = soup.find_all('td', class_='tddatos')
        for i in materia:
            lst.append(i.text.strip())

        # Extraer NRC
        j = 0
        while j < len(lst):
            lstNRC.append(lst[j])
            j += 8

        # Extraer nombres de materias
        j = 2
        while j < len(lst):
            lstMateria.append(lst[j])
            j += 8

        # Extraer nombres de profesores
        j = 7
        while j < len(lst):
            profesor = lst[j].strip().replace("01", "").strip()
            lstProfe.append(profesor)
            j += 8

        # Extraer cupos
        j = 6
        while j < len(lst):
            lstCupo.append(lst[j])
            j += 8

        # Convertir NRC y Cupos a enteros
        lstNRC = list(map(int, lstNRC))
        lstCupo = list(map(int, lstCupo))

        # Mostrar información de cada materia
        print(Fore.CYAN + f'Materia: {lstMateria[0]}' if lstMateria else "Materia: No disponible")

        for x in range(len(lstCupo)):
            if lstCupo[x] > 0:  # Mostrar solo si hay cupos disponibles
                print(Fore.GREEN + 'Cupo disponible')
                print(Fore.YELLOW + f'Profesor: {lstProfe[x]}')
                print(Fore.GREEN + f'NRC: {lstNRC[x]}')
                print(Fore.GREEN + f'Cupos: {lstCupo[x]}\n')

    time.sleep(5)
