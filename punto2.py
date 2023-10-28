import random
import string
import tkinter as tk

# Parámetros del algoritmo genético
tamaño_poblacion = 100
tasa_mutacion = 0.05
num_generaciones = 100000
objetivo = "ALGORITMO GENÉTICO"
elitismo = True

# Funciones del algoritmo genético
def cadena_aleatoria():
    return ''.join(random.choice(string.ascii_uppercase + ' ') for _ in range(len(objetivo)))


def calcular_aptitud(cadena):
    return sum(1 for c1, c2 in zip(cadena, objetivo) if c1 == c2)

def seleccionar_padre(poblacion, aptitudes):
    total_aptitud = sum(aptitudes)
    seleccion = random.uniform(0, total_aptitud)
    suma = 0
    for individuo, aptitud in zip(poblacion, aptitudes):
        suma += aptitud
        if suma >= seleccion:
            return individuo
    return poblacion[-1]

def cruzar(padre1, padre2):
    punto = random.randint(0, len(padre1) - 1)
    return padre1[:punto] + padre2[punto:]

def mutar(cadena):
    if random.random() < tasa_mutacion:
        posicion = random.randint(0, len(cadena) - 1)
        caracter = random.choice(string.ascii_uppercase + ' ')
        return cadena[:posicion] + caracter + cadena[posicion+1:]
    return cadena

# Función para actualizar la interfaz gráfica
def actualizar_interfaz(generacion, mejor_aptitud, mejor_cadena):
    #resultado_label.config(text=f"Generación {generacion} - Mejor aptitud: {mejor_aptitud} - Cadena: {mejor_cadena}")
    #root.update()
    resultado_text.insert(tk.END, f"Generación {generacion} - Mejor aptitud: {mejor_aptitud} - Cadena: {mejor_cadena}\n")
    resultado_text.see(tk.END)  # Hace que la última línea sea visible


# Algoritmo genético
poblacion = [cadena_aleatoria() for _ in range(tamaño_poblacion)]

root = tk.Tk()
root.title("Algoritmo Genetico")

#resultado_label = tk.Label(root, text="")
#resultado_label.pack()
resultado_text = tk.Text(root)
resultado_text.pack()

for generacion in range(num_generaciones):
    aptitudes = [calcular_aptitud(individuo) for individuo in poblacion]

    if max(aptitudes) == len(objetivo):
        mejor_aptitud = max(aptitudes)
        mejor_cadena = poblacion[aptitudes.index(max(aptitudes))]
        actualizar_interfaz(generacion, mejor_aptitud, mejor_cadena)
        print(f"Solución encontrada en la generación {generacion}!")
        break

    actualizar_interfaz(generacion, max(aptitudes), poblacion[aptitudes.index(max(aptitudes))])

    if elitismo:
        elite = [poblacion[aptitudes.index(max(aptitudes))]]
    else:
        elite = []

    nuevos_padres = [seleccionar_padre(poblacion, aptitudes) for _ in range(tamaño_poblacion - len(elite))]

    if len(nuevos_padres) % 2 != 0:
        nuevos_padres.append(random.choice(nuevos_padres))

    poblacion = elite + [mutar(cruzar(nuevos_padres[i], nuevos_padres[i+1])) for i in range(0, len(nuevos_padres), 2)]
else:
    print("No se encontró la solución en el número de generaciones definido.")

root.mainloop()
