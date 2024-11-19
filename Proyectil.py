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
T = sp.symbols('t')

# Ventana principal
Root = tk.Tk()
Root.title("Simulación de Movimiento")
Root.geometry("1000x600")
Root.config(bg="#F0F0F0")

# Definir una fuente personalizada para mejorar la legibilidad
FontTitle = ("Helvetica", 16, "bold")
FontLabels = ("Helvetica", 12)
FontButtons = ("Helvetica", 12, "bold")

# Variables controladas por el usuario
RangoInicio = tk.DoubleVar(value=-3)
RangoFin = tk.DoubleVar(value=3)
PasoTiempo = tk.DoubleVar(value=0.05)
Coeficiente = tk.DoubleVar(value=30)

# Frame para controles con fondo y bordes
FrameControles = ttk.LabelFrame(Root, text="Controles", padding="10 10 10 10")
FrameControles.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
FrameControles.config(height=250)

# Entrada de rango de tiempo con bordes y colores
ttk.Label(FrameControles, text="Inicio Del Rango:", font=FontLabels).grid(row=0, column=0, sticky="w", pady=5)
SpinInicio = ttk.Spinbox(FrameControles, from_=-10, to=10, increment=0.5, textvariable=RangoInicio, width=8, font=FontLabels)
SpinInicio.grid(row=0, column=1, pady=5)

ttk.Label(FrameControles, text="Fin Del Rango:", font=FontLabels).grid(row=1, column=0, sticky="w", pady=5)
SpinFin = ttk.Spinbox(FrameControles, from_=-10, to=10, increment=0.5, textvariable=RangoFin, width=8, font=FontLabels)
SpinFin.grid(row=1, column=1, pady=5)

ttk.Label(FrameControles, text="Coeficiente:", font=FontLabels).grid(row=2, column=0, sticky="w", pady=5)
SpinCoef = ttk.Spinbox(FrameControles, from_=10, to=50, increment=1, textvariable=Coeficiente, width=8, font=FontLabels)
SpinCoef.grid(row=2, column=1, pady=5)

# Botón para iniciar con fondo verde y texto blanco
BtnIniciar = ttk.Button(FrameControles, text="Iniciar Simulación", command=None, style="TButton")
BtnIniciar.grid(row=3, column=0, columnspan=2, pady=10)

# Añadir estilo personalizado al botón
Style = ttk.Style()
Style.configure("TButton", font=FontButtons, padding=6, relief="flat", background="#4CAF50", foreground="green")
Style.map("TButton", background=[("active", "#45a049")])

# Función para iniciar la simulación
def IniciarSimulacion():
    # Obtener valores del usuario
    Inicio = RangoInicio.get()
    Fin = RangoFin.get()
    Paso = PasoTiempo.get()
    Coef = Coeficiente.get()

    # Rango de tiempo
    Tiempo = np.arange(Inicio, Fin + Paso, Paso)

    # Función simbólica de desplazamiento
    DesplazamientoSimbolico = (-1/3) * T**3 + Coef * T

    # Derivar para obtener la velocidad y aceleración
    VelocidadSimbolica = sp.diff(DesplazamientoSimbolico, T)
    AceleracionSimbolica = sp.diff(VelocidadSimbolica, T)

    # Evaluar desplazamiento, velocidad y aceleración
    Desplazamiento = CalcularDesplazamiento(Tiempo, Coef)
    Velocidad = np.array([float(VelocidadSimbolica.subs(T, TVal)) for TVal in Tiempo])
    Aceleracion = np.array([float(AceleracionSimbolica.subs(T, TVal)) for TVal in Tiempo])

    # Hallar los puntos específicos para la leyenda
    VelocidadEnTMenos3 = float(VelocidadSimbolica.subs(T, -3))
    VelocidadEnT0 = float(VelocidadSimbolica.subs(T, 0))
    AceleracionEnTMenos3 = float(AceleracionSimbolica.subs(T, -3))
    AceleracionEnT0 = float(AceleracionSimbolica.subs(T, 0))
    AceleracionEnT3 = float(AceleracionSimbolica.subs(T, 3))
    AlturaMaxima = max(Desplazamiento)

    # Crear figura y ejes
    Fig, Ax = plt.subplots(figsize=(12, 7))
    Ax.set_xlim(Inicio, Fin)
    Ax.set_ylim(min(Desplazamiento) - 10, max(Desplazamiento) + 10)

    # Graficar velocidad y aceleración
    Ax.plot(Tiempo, Velocidad, label="Velocidad (v)", color="green", linestyle="--", linewidth=2)
    Ax.plot(Tiempo, Aceleracion, label="Aceleración (a)", color="red", linestyle=":", linewidth=2)

    # Línea de desplazamiento y marcador
    LineaDesplazamiento, = Ax.plot([], [], 'blue', label="Desplazamiento (s)", linewidth=2)
    Marcador, = Ax.plot([], [], 'r*', markersize=10)

    # Etiquetas y cuadrícula
    Ax.set_title("Movimiento de Proyectil", fontsize=16)
    Ax.set_xlabel("Tiempo (t)", fontsize=14)
    Ax.set_ylabel("Magnitud", fontsize=14)
    Ax.grid(True)

    # Leyenda de los puntos y las ecuaciones
    LeyendaCompleta = (
        f"Velocidad en t=-3: {VelocidadEnTMenos3:.2f}\n"
        f"Velocidad en t=0: {VelocidadEnT0:.2f}\n"
        f"Aceleración en t=-3: {AceleracionEnTMenos3:.2f}\n"
        f"Aceleración en t=0: {AceleracionEnT0:.2f}\n"
        f"Aceleración en t=3: {AceleracionEnT3:.2f}\n"
        f"Altura máxima: {AlturaMaxima:.2f}\n\n"
        f"Ecuación de velocidad: v(t) = {VelocidadSimbolica}\n"
        f"Ecuación de aceleración: a(t) = {AceleracionSimbolica}"
    )

    # Colocar la leyenda combinada en el centro de la gráfica
    Ax.text(0.5, 0.05, LeyendaCompleta, transform=Ax.transAxes, fontsize=12, verticalalignment='center', 
            horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    # Leyenda de los elementos gráficos (Desplazamiento, Velocidad, Aceleración)
    Ax.legend(loc='upper left')

    # Función de inicialización para la animación
    def Init():
        Marcador.set_data([], [])
        LineaDesplazamiento.set_data([], [])
        return Marcador, LineaDesplazamiento

    # Función para actualizar la animación
    def Update(Frame):
        X = Tiempo[Frame]
        Y = Desplazamiento[Frame]
        Marcador.set_data([X], [Y])
        LineaDesplazamiento.set_data(Tiempo[:Frame + 1], Desplazamiento[:Frame + 1])
        return Marcador, LineaDesplazamiento

    TotalFrames = len(Tiempo)
    Intervalo = 1000 * 7 / TotalFrames

    Ani = animation.FuncAnimation(Fig, Update, frames=TotalFrames, init_func=Init, blit=True, interval=Intervalo, repeat=True)

    # Cargar y reproducir sonido
    try:
        WaveObj = sa.WaveObject.from_wave_file("MissileSound.wav")
        WaveObj.play()
    except FileNotFoundError:
        print("Archivo de sonido no encontrado.")

    plt.show()

BtnIniciar.config(command=IniciarSimulacion)

# Iniciar la interfaz gráfica
Root.mainloop()
