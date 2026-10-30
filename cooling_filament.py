import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# paramters for PLA (taken from the first non-AI result I found)

L = 10                  # Circumferance of cylinder [cm]
N = 50                  # Number of elements
ds = L/N                # cm
width = ds             # cm                 # The simulation becomes unstable if this is changed too much 
dt = width                 # s

Tn = 273.15 + 55        # nozzle temp [K] (Must be above ambient!!!)
T_base = 273.15 + 35    # base temp [K]
Te = 273.15 + 19        # ambient temp [K]
T_accept = Te + 5       # Accepted temperature threshold for filament  [K] (must be above ambient !!!)

h_base = 0.02
he = 0.02

k = 0.13                   # Thermal conductivity
rho = 1.24              # density [g/cm^3]
C = 1.8                 # Specific heat capacity [J/(gK)]

# Some handy coefficients
coeff = dt/(rho*C*width)
kp = k/(ds*ds)
gamma = kp*coeff*width
T_ext = coeff*(h_base*T_base + 3*he*Te)


def T_ss(T, ds):
    """Computes the descrete derivative of temperature (T) in space (s) using Euler 2nd order diff"""
    return (T[2] + T[0] - 2*T[1])/(ds*ds)


def one_block_one_step(Tb, Ti, Tf):
    """Computes the temperature of some generic block at time t after 1 timestep"""
    return (1 - 2*gamma - coeff*h_base - 3*coeff*he)*Ti + gamma*(Tf + Tb) + T_ext

def first_block_one_step(Ti):
    """
    Computes the temperature of the very first block at time t after 1 timestep
    (Only for before the circle is complete)
    Insulated back face assumed
    """
    return coeff*(1 - h_base -3*he)*Ti + T_ext


def one_step_printing(Filament):
    """
    Computes 1 timestep of the simulation at time t
    (Only for before the circle is complete)
    """
    Filament.append(Tn)
    filly = Filament.copy()

    filly[0] = first_block_one_step(Filament[0])

    for i in range(1, len(Filament)-1):
        filly[i] = one_block_one_step(Filament[i-1], Filament[i], Filament[i+1])
    
    return filly

def one_step_notprinting(Filament):
    """
    Computes 1 timestep of the simulation at time t
    (after printing is complete and the circle is closed)
    """
    filly = Filament.copy()

    filly[0] = one_block_one_step(Filament[-1], Filament[0], Filament[1])
    filly[-1] = one_block_one_step(Filament[-2], Filament[-1], Filament[0])

    for i in range(1, N-1):
        filly[i] = one_block_one_step(Filament[i-1], Filament[i], Filament[i+1])

    print(filly)
    return filly

phill = [Tn]        # filament at each timestep

phill_list = [np.concat((np.array([Tn]), np.zeros(N-1)))]       # filament at every timestep

for t in range(1, N):
    phill = one_step_printing(phill)
    phill_list.append(np.concat((np.array(phill), np.zeros(N-t-1))))        # add zeros for the non-filament parts so plt doesn't start crying


phill = np.array(phill)
now = 0
while (np.max(phill) > T_accept):           # simulation stops when the filament is below the acceptable temperature
    phill = one_step_notprinting(phill)
    phill_list.append(phill)
    print(now)
    now +=1



fig, ax = plt.subplots(figsize=(25, 7))
ax.set_xlabel("Length of filament")
#scatter = ax.scatter(np.arange(N), np.zeros(N), s=100, c=phill_list[0], cmap="viridis", vmin=Te, vmax=Tn, marker="s")
scatter = ax.pcolormesh(ds*np.arange(N), [0, 1], [phill_list[0], phill_list[0]], vmin=Te, vmax=Tn)
cbar = fig.colorbar(scatter, ax=ax)

def update(frame):
    scatter.set_array([phill_list[frame], phill_list[frame]])
    return scatter

anim = FuncAnimation(fig, update, frames=(len(phill_list)-1), interval=1000*dt, blit=False, repeat=False)

plt.show()


        

