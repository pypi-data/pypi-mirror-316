from .cursos import cursos

def duracion_total():
    return sum(curso.duration for curso in cursos)
