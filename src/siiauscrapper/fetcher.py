import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from .models import CourseAvailability


def _parse_int(value: str) -> int:
    digits = re.sub(r"[^0-9]", "", value or "")
    return int(digits) if digits else 0


def _parse_course_row(cells, url: str) -> Optional[CourseAvailability]:
    if len(cells) < 8:
        return None

    nrc_text = cells[0].get_text(strip=True)
    materia_text = cells[2].get_text(strip=True)
    cupo_text = cells[6].get_text(strip=True)
    profesor_text = cells[7].get_text(strip=True).replace("01", "").strip()

    nrc = _parse_int(nrc_text)
    cupo = _parse_int(cupo_text)

    if nrc == 0:
        return None

    return CourseAvailability(
        nrc=nrc,
        materia=materia_text or "Desconocida",
        cupo=cupo,
        profesor=profesor_text or "Desconocido",
        url=url,
    )


def parse_course_table(html: str, url: str) -> List[CourseAvailability]:
    soup = BeautifulSoup(html, "html.parser")
    courses: List[CourseAvailability] = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td", class_="tddatos")
        if not cells:
            continue

        parsed = _parse_course_row(cells, url)
        if parsed:
            courses.append(parsed)

    if courses:
        return courses

    flat_cells = [cell.get_text(strip=True) for cell in soup.find_all("td", class_="tddatos")]
    for index in range(0, len(flat_cells), 8):
        block = flat_cells[index:index + 8]
        if len(block) < 8:
            continue
        parsed = _parse_course_row([BeautifulSoup(f"<td>{value}</td>", "html.parser").td for value in block], url)
        if parsed:
            courses.append(parsed)

    return courses


def fetch_course_availability(url: str, timeout: int = 10, verify: bool = True) -> List[CourseAvailability]:
    response = requests.get(url, timeout=timeout, verify=verify)
    response.raise_for_status()
    return parse_course_table(response.text, url)
