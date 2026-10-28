import numpy as np
import matplotlib.pyplot as plt

L = 10                  # Circumferance of cylinder [cm]
N = 10                  # Number of elements
ds = L/N                # cm
width = 0.1             # cm
dt = width                 # s
time_steps = 10         # s

Tn = 273.15 + 50        # nozzle temp [K]
T_base = 273.15 + 35    # base temp [K]
Te = 273.15 + 19        # ambient temp [K]
T_accept = Te + 5       # Accepted temperature threshold for filament  [K]

h_base = 0.2
he = 0.2

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

domain = np.zeros((N, time_steps))

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

for t in range(1, N):
    print(t)
    phill = one_step_printing(phill)

phill = np.array(phill)
while np.max(phill) > T_accept:
    phill = one_step_notprinting(phill)






        

