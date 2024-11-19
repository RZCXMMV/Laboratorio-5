import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import simpleaudio as sa
import sympy as sp
import tkinter as tk
from tkinter import ttk

# Función de desplazamiento (posición)
def CalcularDesplazamiento(Tiempo, Coeficiente):
    return (-1/3) * Tiempo**3 + Coeficiente * Tiempo

# Crear la variable simbólica 't'
t = sp.symbols('t')

# Ventana principal
root = tk.Tk()
root.title("Simulación de Movimiento")

# Variables controladas por el usuario
RangoInicio = tk.DoubleVar(value=-3)
RangoFin = tk.DoubleVar(value=3)
PasoTiempo = tk.DoubleVar(value=0.05)
Coeficiente = tk.DoubleVar(value=30)

# Frame para controles
frame_controles = ttk.LabelFrame(root, text="Controles")
frame_controles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Entrada de rango de tiempo
ttk.Label(frame_controles, text="Rango Inicio (t):").grid(row=0, column=0, sticky="w")
spin_inicio = ttk.Spinbox(frame_controles, from_=-10, to=10, increment=0.5, textvariable=RangoInicio, width=8)
spin_inicio.grid(row=0, column=1)

ttk.Label(frame_controles, text="Rango Fin (t):").grid(row=1, column=0, sticky="w")
spin_fin = ttk.Spinbox(frame_controles, from_=-10, to=10, increment=0.5, textvariable=RangoFin, width=8)
spin_fin.grid(row=1, column=1)

# Entrada del coeficiente
ttk.Label(frame_controles, text="Coeficiente:").grid(row=2, column=0, sticky="w")
spin_coef = ttk.Spinbox(frame_controles, from_=10, to=50, increment=1, textvariable=Coeficiente, width=8)
spin_coef.grid(row=2, column=1)

# Botón para iniciar
btn_iniciar = ttk.Button(frame_controles, text="Iniciar Simulación")
btn_iniciar.grid(row=3, column=0, columnspan=2, pady=5)

# Frame para la gráfica
frame_grafica = ttk.LabelFrame(root, text="Simulación")
frame_grafica.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Función para iniciar la simulación
def IniciarSimulacion():
    # Obtener valores del usuario
    inicio = RangoInicio.get()
    fin = RangoFin.get()
    paso = PasoTiempo.get()
    coef = Coeficiente.get()

    # Rango de tiempo
    Tiempo = np.arange(inicio, fin + paso, paso)

    # Función simbólica de desplazamiento
    DesplazamientoSimbolico = (-1/3) * t**3 + coef * t

    # Derivar para obtener la velocidad y aceleración
    VelocidadSimbolica = sp.diff(DesplazamientoSimbolico, t)
    AceleracionSimbolica = sp.diff(VelocidadSimbolica, t)

    # Evaluar desplazamiento, velocidad y aceleración
    Desplazamiento = CalcularDesplazamiento(Tiempo, coef)
    Velocidad = np.array([float(VelocidadSimbolica.subs(t, t_val)) for t_val in Tiempo])
    Aceleracion = np.array([float(AceleracionSimbolica.subs(t, t_val)) for t_val in Tiempo])

    # Hallar los puntos específicos para la leyenda
    VelocidadEnTmenos3 = float(VelocidadSimbolica.subs(t, -3))
    VelocidadEnT0 = float(VelocidadSimbolica.subs(t, 0))
    AceleracionEnTmenos3 = float(AceleracionSimbolica.subs(t, -3))
    AceleracionEnT0 = float(AceleracionSimbolica.subs(t, 0))
    AceleracionEnT3 = float(AceleracionSimbolica.subs(t, 3))
    AlturaMaxima = max(Desplazamiento)

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(inicio, fin)
    ax.set_ylim(min(Desplazamiento) - 10, max(Desplazamiento) + 10)
    
    # Graficar velocidad y aceleración
    ax.plot(Tiempo, Velocidad, label="Velocidad (v)", color="green", linestyle="--", linewidth=2)
    ax.plot(Tiempo, Aceleracion, label="Aceleración (a)", color="red", linestyle=":", linewidth=2)

    # Línea de desplazamiento y marcador
    linea_desplazamiento, = ax.plot([], [], 'blue', label="Desplazamiento (s)", linewidth=2)
    marker, = ax.plot([], [], 'r*', markersize=10)

    # Etiquetas y cuadrícula
    ax.set_title("Movimiento de Proyectil", fontsize=16)
    ax.set_xlabel("Tiempo (t)", fontsize=14)
    ax.set_ylabel("Magnitud", fontsize=14)
    ax.grid(True)

    # Leyenda combinada de los puntos y las ecuaciones
    leyenda_completa = (
        f"Velocidad en t=-3: {VelocidadEnTmenos3:.2f}\n"
        f"Velocidad en t=0: {VelocidadEnT0:.2f}\n"
        f"Aceleración en t=-3: {AceleracionEnTmenos3:.2f}\n"
        f"Aceleración en t=0: {AceleracionEnT0:.2f}\n"
        f"Aceleración en t=3: {AceleracionEnT3:.2f}\n"
        f"Altura máxima: {AlturaMaxima:.2f}\n\n"
        f"Ecuación de velocidad: v(t) = {VelocidadSimbolica}\n"
        f"Ecuación de aceleración: a(t) = {AceleracionSimbolica}"
    )

    # Colocar la leyenda combinada en el centro de la gráfica
    ax.text(0.5, 0.05, leyenda_completa, transform=ax.transAxes, fontsize=12, verticalalignment='center', 
            horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    # Leyenda de los elementos gráficos (Desplazamiento, Velocidad, Aceleración)
    ax.legend(loc='upper left')

    # Función de inicialización para la animación
    def init():
        marker.set_data([], [])
        linea_desplazamiento.set_data([], [])
        return marker, linea_desplazamiento

    # Función para actualizar la animación
    def update(frame):
        x = Tiempo[frame]
        y = Desplazamiento[frame]
        marker.set_data([x], [y])
        linea_desplazamiento.set_data(Tiempo[:frame + 1], Desplazamiento[:frame + 1])
        return marker, linea_desplazamiento

    total_frames = len(Tiempo)
    interval = 1000 * 7 / total_frames

    ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=interval, repeat=False)

    # Cargar y reproducir sonido
    try:
        wave_obj = sa.WaveObject.from_wave_file("MissileSound.wav")
        wave_obj.play()
    except FileNotFoundError:
        print("Archivo de sonido no encontrado.")

    plt.show()

btn_iniciar.config(command=IniciarSimulacion)

# Iniciar la interfaz gráfica
root.mainloop()