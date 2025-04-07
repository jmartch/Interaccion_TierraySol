import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# Constantes físicas
G = 6.67430e-11
M_sol = 1.989e30
UA = 1.496e11

# Parámetros de simulación
dt = 3600 * 24  # 1 día
T_total = 3.154e7 * 2  # 2 años
N = int(T_total // dt)

# Configuración de planetas [masa, distancia inicial (UA), velocidad (km/s), color]
planetas = {
    'Mercurio': [3.3011e23, 0.387, 47.36, 'gray'],
    'Venus': [4.8675e24, 0.723, 35.02, 'orange'],
    'Tierra': [5.972e24, 1.0, 29.78, 'blue'],
    'Marte': [6.417e23, 1.524, 24.07, 'red']
}

# Inicialización de estados
estados = {}
for nombre, (masa, distancia, velocidad, color) in planetas.items():
    estados[nombre] = {
        'masa': masa,
        'color': color,
        'pos': np.array([distancia * UA, 0.0]),
        'vel': np.array([0.0, velocidad * 1000]),
        'trayectoria': np.zeros((N+1, 2))
    }
    estados[nombre]['trayectoria'][0] = estados[nombre]['pos']

def calcular_aceleracion(pos, masa_central):
    r = np.linalg.norm(pos)
    factor = -G * masa_central / r**3
    return factor * pos

# Simulación
for i in range(1, N+1):
    for nombre in planetas:
        planeta = estados[nombre]
        a = calcular_aceleracion(planeta['pos'], M_sol)
        nueva_pos = planeta['pos'] + planeta['vel'] * dt + 0.5 * a * dt**2
        nueva_a = calcular_aceleracion(nueva_pos, M_sol)
        planeta['vel'] += 0.5 * (a + nueva_a) * dt
        planeta['pos'] = nueva_pos
        planeta['trayectoria'][i] = nueva_pos

# Configuración de la figura
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title("Sistema Solar Interno - Órbitas Completas", fontsize=16, pad=20)

# Dibujar el Sol
ax.plot(0, 0, 'yo', markersize=25, label='Sol')

# Dibujar todas las trayectorias completas primero (líneas estáticas)
for nombre in planetas:
    color = estados[nombre]['color']
    trayectoria_ua = estados[nombre]['trayectoria'] / UA
    ax.plot(trayectoria_ua[:, 0], trayectoria_ua[:, 1], '-', 
            color=color, alpha=0.5, lw=1.5, label=nombre)

# Elementos de animación (solo los planetas como puntos móviles)
puntos = {}
for nombre in planetas:
    color = estados[nombre]['color']
    puntos[nombre], = ax.plot([], [], 'o', color=color, markersize=10)

ax.legend(loc='upper right', fontsize=12)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, 
                   fontsize=14, bbox=dict(facecolor='white', alpha=0.8))

def init():
    for nombre in planetas:
        puntos[nombre].set_data([], [])
    time_text.set_text('')
    return list(puntos.values()) + [time_text]

def update(frame):
    frame = frame % N  # Esto crea el bucle infinito
    
    for nombre in planetas:
        pos_actual_ua = estados[nombre]['trayectoria'][frame] / UA
        puntos[nombre].set_data([pos_actual_ua[0]], [pos_actual_ua[1]])
    
    days = int(frame * dt / (3600 * 24))
    time_text.set_text(f'Días: {days}\nAños: {days/365:.2f}')
    
    return list(puntos.values()) + [time_text]

# Configuración de la animación
ani = animation.FuncAnimation(
    fig, update, frames=N, init_func=init,
    interval=20, blit=True, repeat=True
)

plt.tight_layout()
plt.show()