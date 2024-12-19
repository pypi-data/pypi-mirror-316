class Curso:

    def __init__(self, name, duration, link):
        self.name = name
        self.link = link
        self.duration = duration

    def __repr__(self):
        return f"{self.name}, [{self.duration} horas], ({self.link})"

cursos = [
    Curso("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion_a_linux/"),
    Curso("Personalización de entornos", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Curso("Introducción al hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
    Curso("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/")
]

def listar_cursos():
    for curso in cursos:
        print(curso)

def buscar_curso_por_nombre(nombre):
    for curso in cursos:
        if curso.name == nombre:
            return curso

    return None
