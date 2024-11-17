import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import simpleaudio as sa
import sympy as sp

# Función de desplazamiento (posición)
def CalcularDesplazamiento(Tiempo):
    return (-1/3) * Tiempo**3 + 30 * Tiempo

# Crear la variable simbólica 't'
t = sp.symbols('t')

# Definir la función simbólica de desplazamiento
DesplazamientoSimbolico = (-1/3) * t**3 + 30 * t

# Derivar para obtener la velocidad (primera derivada)
VelocidadSimbolica = sp.diff(DesplazamientoSimbolico, t)

# Derivar para obtener la aceleración (segunda derivada)
AceleracionSimbolica = sp.diff(VelocidadSimbolica, t)

# Función para evaluar las expresiones simbólicas en un valor de t
def EvaluarFuncion(funcion, valor_t):
    return float(funcion.subs(t, valor_t))

# Rango de tiempo para la animación de -3 a 3 con un paso de 0.05
Tiempo = np.arange(-3, 3.05, 0.05)  # De -3 a 3 con incremento de 0.05

# Cálculo de desplazamiento, velocidad y aceleración
Desplazamiento = CalcularDesplazamiento(Tiempo)
Velocidad = np.array([EvaluarFuncion(VelocidadSimbolica, t_val) for t_val in Tiempo])
Aceleracion = np.array([EvaluarFuncion(AceleracionSimbolica, t_val) for t_val in Tiempo])

# Crear la figura y los ejes para la animación
fig, ax = plt.subplots(figsize=(12, 7))  # Aumentar tamaño de la figura

# Definir límites de la gráfica para el eje X de -3 a 3
ax.set_xlim(-3, 3)

# Ampliamos los límites del eje Y para que todo sea visible
ax.set_ylim(min(Desplazamiento) - 10, max(Desplazamiento) + 10)

# Graficar las curvas completas de Velocidad y Aceleración (estáticas)
ax.plot(Tiempo, Velocidad, label="Velocidad (v)", color="green", linestyle="--", linewidth=2)
ax.plot(Tiempo, Aceleracion, label="Aceleración (a)", color="red", linestyle=":", linewidth=2)

# Línea para el desplazamiento (que se trazará progresivamente)
linea_desplazamiento, = ax.plot([], [], 'blue', label="Desplazamiento (s)", linewidth=2)

# Crear un marcador de desplazamiento (representado como un asterisco '*')
marker, = ax.plot([], [], 'r*', markersize=10)  # Marcador rojo

# Agregar títulos y etiquetas
ax.set_title("Lanzamiento de Proyectil: Desplazamiento, Velocidad y Aceleración", fontsize=16)
ax.set_xlabel("Tiempo (t) en segundos", fontsize=14)
ax.set_ylabel("Magnitud", fontsize=14)

# Mostrar la cuadrícula
ax.grid(True)

# Leyenda en la gráfica
ax.legend(loc='upper left')

# Función de inicialización de la animación
def init():
    marker.set_data([], [])
    linea_desplazamiento.set_data([], [])
    return marker, linea_desplazamiento

# Función de actualización para la animación
def update(frame):
    # Actualizar el marcador rojo (proyectil en movimiento)
    x = Tiempo[frame]
    y = Desplazamiento[frame]
    marker.set_data([x], [y])
    
    # Actualizar la línea azul para trazar el desplazamiento gradualmente
    linea_desplazamiento.set_data(Tiempo[:frame+1], Desplazamiento[:frame+1])
    
    return marker, linea_desplazamiento

# Calcular el intervalo necesario para que la animación dure 10 segundos
total_frames = len(Tiempo)
interval = 1000 * 8 / total_frames  # 10 segundos / total_frames, convertido a milisegundos

# Crear la animación (durará 10 segundos)
ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True, interval=interval, repeat=False)

# Cargar y reproducir el sonido del arranque del proyectil
wave_obj = sa.WaveObject.from_wave_file("MissileSound.wav")
play_obj = wave_obj.play()

# Establecer marcas personalizadas en el eje X
ax.set_xticks([-3, 0, 3])  # Marcas de tiempo personalizadas

# Mostrar la gráfica
plt.show()
