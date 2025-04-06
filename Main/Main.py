import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constantes físicas
G = 6.67430e-11
M_sol = 1.989e30
M_tierra = 5.972e24
UA = 1.496e11
dt = 3600 * 24  # 1 día
T_total = 3.154e7  # 1 año
N = int(T_total // dt)

# Condiciones iniciales
x = UA
y = 0
vx = 0
vy = 29.783e3

# Almacenar trayectoria para animar
x_verlet, y_verlet = [x], [y]
x_v, y_v = x, y
vx_v, vy_v = vx, vy

def calcular_aceleracion(x, y):
    r = np.sqrt(x**2 + y**2)
    a_mag = -G * M_sol / r**2
    return a_mag * (x / r), a_mag * (y / r)

# Simulación y guardado de posiciones
for _ in range(N):
    ax, ay = calcular_aceleracion(x_v, y_v)
    x_nuevo = x_v + vx_v * dt + 0.5 * ax * dt**2
    y_nuevo = y_v + vy_v * dt + 0.5 * ay * dt**2
    ax_nuevo, ay_nuevo = calcular_aceleracion(x_nuevo, y_nuevo)
    vx_v += 0.5 * (ax + ax_nuevo) * dt
    vy_v += 0.5 * (ay + ay_nuevo) * dt
    x_v, y_v = x_nuevo, y_nuevo
    x_verlet.append(x_v)
    y_verlet.append(y_v)

# Crear animación
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.2*UA, 1.2*UA)
ax.set_ylim(-1.2*UA, 1.2*UA)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Simulación Tierra-Sol (Verlet)")

line, = ax.plot([], [], 'b-', lw=1, label="Órbita")
planet, = ax.plot([], [], 'bo', label="Tierra")
sun = ax.plot(0, 0, 'yo', markersize=12, label="Sol")

def init():
    line.set_data([], [])
    planet.set_data([], [])
    return line, planet

def update(frame):
    line.set_data(x_verlet[:frame], y_verlet[:frame])
    planet.set_data(x_verlet[frame], y_verlet[frame])
    return line, planet

ani = animation.FuncAnimation(
    fig, update, frames=len(x_verlet), init_func=init,
    interval=10, blit=True, repeat=True
)

plt.legend()
plt.show()
