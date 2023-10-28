import random
import math
import tkinter as tk
from tkinter import ttk

# Datos de las conferencias
conferencias = [
    {"nombre": "Conferencia 1", "duracion": 1.5, "horarioPreferido": "Mañana", "asientosDisponibles": 50},
    {"nombre": "Conferencia 2", "duracion": 2, "horarioPreferido": "Tarde", "asientosDisponibles": 100},
    {"nombre": "Conferencia 3", "duracion": 2, "horarioPreferido": "Tarde", "asientosDisponibles": 80},
    {"nombre": "Conferencia 4", "duracion": 1.5, "horarioPreferido": "Tarde", "asientosDisponibles": 30},
    {"nombre": "Conferencia 5", "duracion": 1.5, "horarioPreferido": "Tarde", "asientosDisponibles": 60},
    # Agrega datos para las otras conferencias
    # Asegúrate de agregar los datos de las 15 conferencias
]

# Datos de las salas de conferencias y horarios
salas = ["Sala 1", "Sala 2", "Sala 3"]
horarios = ["Mañana", "Tarde", "Noche"]

# Función para calcular la asistencia total de una programación
def calcular_asistencia_total(programacion):
    asistencia_total = 0
    for conferencia in programacion:
        asistencia_total += conferencia["asistentes"]
    return asistencia_total

# Función para generar una programación aleatoria
def generar_programacion_aleatoria(conferencias, salas, horarios):
    programacion = []
    for conferencia in conferencias:
        sala = random.choice(salas)
        horario = random.choice(horarios)
        programacion.append({"conferencia": conferencia, "sala": sala, "horario": horario, "asistentes": 0})
    return programacion

# Función para aplicar el algoritmo de recocido simulado
def recocido_simulado(conferencias, salas, horarios, temperatura_inicial, enfriamiento):
    programacion_actual = generar_programacion_aleatoria(conferencias, salas, horarios)
    asistencia_actual = calcular_asistencia_total(programacion_actual)

    mejor_programacion = list(programacion_actual)
    mejor_asistencia = asistencia_actual

    temperatura = temperatura_inicial

    while temperatura > 1:
        i, j = random.sample(range(len(conferencias)), 2)

        programacion_actual[i]["horario"], programacion_actual[j]["horario"] = (
            programacion_actual[j]["horario"],
            programacion_actual[i]["horario"],
        )

        nueva_asistencia = calcular_asistencia_total(programacion_actual)
        diferencia = nueva_asistencia - asistencia_actual

        if diferencia > 0 or random.random() < math.exp(diferencia / temperatura):
            asistencia_actual = nueva_asistencia
            if asistencia_actual > mejor_asistencia:
                mejor_programacion = list(programacion_actual)
                mejor_asistencia = asistencia_actual
        else:
            programacion_actual[i]["horario"], programacion_actual[j]["horario"] = (
                programacion_actual[j]["horario"],
                programacion_actual[i]["horario"],
            )

        temperatura *= enfriamiento

    # Actualizar el horario preferido y los asientos disponibles en la lista de conferencias
    for programacion_conferencia in mejor_programacion:
        conferencia = programacion_conferencia["conferencia"]
        conferencia["horarioPreferido"] = programacion_conferencia["horario"]
        conferencia["asientosDisponibles"] -= programacion_conferencia["asistentes"]

    return mejor_programacion
# Función para mostrar la programación óptima en una ventana de GUI
def mostrar_programacion(programacion_optima):
    ventana = tk.Tk()
    ventana.title("Planificación de Conferencias")
   
    asistencia_label = tk.Label(ventana, text=f"temperatura: {temperatura_inicial}", font=("Arial", 16, "bold"))
    asistencia_label.pack()

    tabla = ttk.Treeview(ventana, columns=("Nombre de la conferencia", "Duración (horas)", "Horario Preferido", "Sala de Conferencia", "Asientos disponibles"))
    tabla.heading("#1", text="Nombre de la conferencia")
    tabla.heading("#2", text="Duración (horas)")
    tabla.heading("#3", text="Horario Preferido")
    tabla.heading("#4", text="Sala de Conferencia")
    tabla.heading("#5", text="Asientos disponibles")

    # Configurar el estilo de las cabeceras
    style = ttk.Style()
    style.configure("Treeview.Heading", foreground="blue", background="blue")

    # Configurar el estilo de las filas
    style.map("Treeview", foreground=[("selected", "black")], background=[("selected", "white")])

    tabla.tag_configure('blue', background='white')
    tabla.pack()

    for conferencia in programacion_optima:
        duracion_horas = conferencia["conferencia"]["duracion"]
        asientos_disponibles = conferencia["conferencia"]["asientosDisponibles"]
        tabla.insert("", "end", values=(conferencia["conferencia"]["nombre"], duracion_horas, conferencia["conferencia"]["horarioPreferido"], conferencia["sala"], asientos_disponibles), tags=('transparent'))

  
  
    # Configurar la alineación de las columnas (centrar todas)
    tabla.column("#1", anchor="center")
    tabla.column("#2", anchor="center")
    tabla.column("#3", anchor="center")
    tabla.column("#4", anchor="center")
    tabla.column("#5", anchor="center")
 

    ventana.mainloop()

# Ejemplo de uso
temperatura_inicial = 1000
enfriamiento = 0.98
programacion_optima = recocido_simulado(conferencias, salas, horarios, temperatura_inicial, enfriamiento)
mostrar_programacion(programacion_optima)
