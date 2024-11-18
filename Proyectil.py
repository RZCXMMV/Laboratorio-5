import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sp
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Crear la variable simbólica 't'
t = sp.symbols('t')

# Función de desplazamiento (posición)
def calcular_desplazamiento(t, coeficiente):
    return (-1/3) * t**3 + coeficiente * t

# Ventana principal
root = tk.Tk()
root.title("Simulación de Movimiento")
root.geometry("800x600")  # Dimensiones iniciales
root.state('zoomed')  # Pantalla completa

# Crear una imagen de prueba simple (una imagen blanca de 800x600 píxeles)
bg_image = Image.new("RGB", (root.winfo_screenwidth(), root.winfo_screenheight()), color=(255, 255, 255))  # Blanco
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Frame principal
frame_menu = tk.Frame(root, bg="#ffffff", relief="raised", bd=5)
frame_menu.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

# Etiqueta de bienvenida
titulo = tk.Label(frame_menu, text="Simulación de Movimiento", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333")
titulo.pack(pady=20)

# Botón para iniciar simulación
btn_simulacion = tk.Button(
    frame_menu, text="Iniciar Simulación", font=("Arial", 16),
    bg="#4caf50", fg="white", width=20, height=2, command=lambda: iniciar_simulacion(root)
)
btn_simulacion.pack(pady=10)

# Botón para calcular resultados
btn_calcular = tk.Button(
    frame_menu, text="Calcular Resultados", font=("Arial", 16),
    bg="#2196f3", fg="white", width=20, height=2, command=lambda: calcular_resultados()
)
btn_calcular.pack(pady=10)

# Botón para salir
btn_salir = tk.Button(
    frame_menu, text="Salir", font=("Arial", 16),
    bg="#f44336", fg="white", width=20, height=2, command=root.quit
)
btn_salir.pack(pady=10)

# Función para calcular resultados
def calcular_resultados():
    resultado_window = tk.Toplevel(root)
    resultado_window.title("Calcular Resultados")
    resultado_window.geometry("600x400")
    resultado_label = tk.Label(resultado_window, text="Esta sección estará disponible pronto.", font=("Arial", 14))
    resultado_label.pack(pady=20)

# Función para iniciar simulación
def iniciar_simulacion(parent):
    # Crear nueva ventana para simulación
    simulacion_window = tk.Toplevel(parent)
    simulacion_window.title("Simulación de Movimiento")
    simulacion_window.geometry("800x600")

    # Variables controladas por el usuario
    rango_inicio = tk.DoubleVar(value=-3)
    rango_fin = tk.DoubleVar(value=3)
    coeficiente = tk.DoubleVar(value=30)

    # Frame para controles
    frame_controles = ttk.LabelFrame(simulacion_window, text="Controles")
    frame_controles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Entrada de rango de tiempo
    ttk.Label(frame_controles, text="Rango Inicio (t):").grid(row=0, column=0, sticky="w")
    spin_inicio = ttk.Spinbox(frame_controles, from_=-10, to=10, increment=0.5, textvariable=rango_inicio, width=8)
    spin_inicio.grid(row=0, column=1)

    ttk.Label(frame_controles, text="Rango Fin (t):").grid(row=1, column=0, sticky="w")
    spin_fin = ttk.Spinbox(frame_controles, from_=-10, to=10, increment=0.5, textvariable=rango_fin, width=8)
    spin_fin.grid(row=1, column=1)

    # Entrada del coeficiente
    ttk.Label(frame_controles, text="Coeficiente:").grid(row=2, column=0, sticky="w")
    spin_coef = ttk.Spinbox(frame_controles, from_=10, to=50, increment=1, textvariable=coeficiente, width=8)
    spin_coef.grid(row=2, column=1)

    # Botón para iniciar animación
    btn_iniciar = ttk.Button(frame_controles, text="Iniciar Animación")
    btn_iniciar.grid(row=3, column=0, columnspan=2, pady=5)

    # Función para ejecutar la animación
    def iniciar_animacion():
        inicio = rango_inicio.get()
        fin = rango_fin.get()
        coef = coeficiente.get()

        tiempo = np.linspace(inicio, fin, 200)
        desplazamiento = calcular_desplazamiento(tiempo, coef)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(inicio, fin)
        ax.set_ylim(min(desplazamiento) - 10, max(desplazamiento) + 10)

        linea_desplazamiento, = ax.plot([], [], 'blue', label="Desplazamiento (s)", linewidth=2)
        marcador, = ax.plot([], [], 'ro', markersize=8)

        def init():
            marcador.set_data([], [])
            linea_desplazamiento.set_data([], [])
            return marcador, linea_desplazamiento

        def update(frame):
            x = tiempo[frame]
            y = desplazamiento[frame]
            marcador.set_data([x], [y])
            linea_desplazamiento.set_data(tiempo[:frame + 1], desplazamiento[:frame + 1])
            return marcador, linea_desplazamiento

        ani = animation.FuncAnimation(fig, update, frames=len(tiempo), init_func=init, blit=True, interval=50, repeat=False)
        plt.show()

    btn_iniciar.config(command=iniciar_animacion)

# Ejecutar la interfaz gráfica
root.mainloop()
