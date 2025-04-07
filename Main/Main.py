import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constantes
G = 6.67430e-11
UA = 1.496e11
dt = 3600 * 24  # 1 día
T_total = 3.154e7  # 1 año
N = int(T_total // dt)

# Cuerpos: Sol, Mercurio, Venus, Tierra, Marte
names = ['Sol', 'Mercurio', 'Venus', 'Tierra', 'Marte']
masses = np.array([1.989e30, 3.30e23, 4.869e24, 5.972e24, 6.419e23])
positions = np.array([
    [0.0, 0.0],                 # Sol
    [0.387 * UA, 0.0],          # Mercurio
    [0.723 * UA, 0.0],          # Venus
    [1.0 * UA, 0.0],            # Tierra
    [-1.524 * UA, 0.0],         # Marte
])
velocities = np.array([
    [0.0, 0.0],                  # Sol
    [0.0, -47.4e3],              # Mercurio
    [0.0, -35.02e3],             # Venus
    [0.0, 29.783e3],             # Tierra
    [0.0, 24.077e3],             # Marte
])

n_bodies = len(masses)
trajectories = [ [positions[i].copy()] for i in range(n_bodies) ]

#Sumatoria de aceleraciones de cada planeta con cada otro planeta
def compute_accelerations(positions):
    accelerations = np.zeros_like(positions)
    for i in range(n_bodies):
        for j in range(n_bodies):
            if i != j:
                r_vec = positions[j] - positions[i]
                r = np.linalg.norm(r_vec)
                if r != 0:
                    accelerations[i] += G * masses[j] * r_vec / r**3
    return accelerations

# Simulación
for _ in range(N):
    acc = compute_accelerations(positions)
    positions += velocities * dt + 0.5 * acc * dt**2
    acc_new = compute_accelerations(positions)
    velocities += 0.5 * (acc + acc_new) * dt
    for i in range(n_bodies):
        trajectories[i].append(positions[i].copy())

# Animación
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2*UA, 2*UA)
ax.set_ylim(-2*UA, 2*UA)
ax.set_aspect('equal')
ax.set_title("Simulación  ")
colors = ['yellow', 'gray', 'orange', 'blue', 'red']
lines = [ax.plot([], [], '-', color=colors[i])[0] for i in range(n_bodies)]
bodies = [ax.plot([], [], 'o', color=colors[i], label=names[i])[0] for i in range(n_bodies)]

def init():
    for line, body in zip(lines, bodies):
        line.set_data([], [])
        body.set_data([], [])
    return lines + bodies

def update(frame):
    for i in range(n_bodies):
        traj = np.array(trajectories[i])
        max_frame = min(frame, len(traj) - 1)  # 👈 Protect against out-of-bounds

        lines[i].set_data(traj[:max_frame, 0], traj[:max_frame, 1])
        bodies[i].set_data([traj[max_frame, 0]], [traj[max_frame, 1]])
    return lines + bodies

ani = animation.FuncAnimation(fig, update, frames=N, init_func=init,
                              interval=10, blit=True, repeat=True)

plt.legend()
plt.grid(True)
plt.show()
