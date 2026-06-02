from dataclasses import dataclass

@dataclass
class CourseAvailability:
    nrc: int
    materia: str
    cupo: int
    profesor: str
    url: str
