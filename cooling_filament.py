import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L = 100                  # Circumferance of cylinder [cm]
N = 100                  # Number of elements
ds = L/N                # cm
width = 0.1             # cm
dt = width                 # s

Tn = 273.15 + 50        # nozzle temp [K]
T_base = 273.15 + 35    # base temp [K]
Te = 273.15 + 19        # ambient temp [K]
T_accept = Te + 5       # Accepted temperature threshold for filament  [K]

h_base = 0.002
he = 0.002

k = 1                   # Thermal conductivity
rho = 1.24              # density [g/cm^3]
C = 1.8                 # Specific heat capacity [J/(gK)]
coeff = dt/(rho*C*width)
kp = k/(ds*ds)
gamma = kp*coeff*width
T_ext = coeff*(h_base*T_base + 3*he*Te)
print(coeff)


def T_ss(T, ds):
    return (T[2] + T[0] - 2*T[1])/(ds*ds)


def one_block_one_step(Tb, Ti, Tf):
    return (1 - 2*gamma - coeff*h_base - 3*coeff*he)*Ti + gamma*(Tf + Tb) + T_ext

def first_block_one_step(Ti):
    return coeff*(1 - h_base -3*he)*Ti + T_ext


def one_step_printing(Filament):
    Filament.append(Tn)
    filly = Filament.copy()

    filly[0] = first_block_one_step(Filament[0])

    for i in range(1, len(Filament)-1):
        filly[i] = one_block_one_step(Filament[i-1], Filament[i], Filament[i+1])

    print(filly)
    return filly

def one_step_notprinting(Filament):
    filly = Filament.copy()

    filly[0] = one_block_one_step(Filament[-1], Filament[0], Filament[1])
    filly[-1] = one_block_one_step(Filament[-2], Filament[-1], Filament[0])

    for i in range(1, L-1):
        filly[i] = one_block_one_step(Filament[i-1], Filament[i], Filament[i+1])

    print(filly)
    return filly

phill = [Tn]

phill_list = [np.concat((np.array([Tn]), np.zeros(N-1)))]

for t in range(1, N):
    print(t)
    phill = one_step_printing(phill)
    phill_list.append(np.concat((np.array(phill), np.zeros(N-t-1))))

print(phill_list)
print()
print()

phill = np.array(phill)
while np.max(phill) > T_accept:
    phill = one_step_notprinting(phill)
    phill_list.append(phill)

print(phill_list)




fig, ax = plt.subplots(figsize=(25, 1))
#scatter = ax.scatter(np.arange(N), np.zeros(N), s=100, c=phill_list[0], cmap="viridis", vmin=Te, vmax=Tn, marker="s")
scatter = ax.pcolormesh(ds*np.arange(N), dt*np.arange(len(phill_list)), phill_list, vmin=Te, vmax=Tn)
cbar = fig.colorbar(scatter, ax=ax)

#def update(frame):
#    scatter.set_array(phill_list[frame])
#    return scatter
#
#anim = FuncAnimation(fig, update, frames=(len(phill_list)-1), interval=200, blit=False, repeat=False)

plt.show()


        

