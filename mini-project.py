import numpy as np
import matplotlib.pyplot as plt
from control import ss 

r_m = 0.04         # m   
mu_r = 0.1
mu_lx = 0.1
mu_ly = 0.1
K_m = 1 
J_m = 1
R_m = 1
L_m = 1
m = 0.5         # kg

def kinematics(theta_l, theta_r, theta_l_dot, theta_r_dot, x0, y0):
    x = x0 + r_m*(theta_l + theta_r)/2
    y = y0 + r_m*(theta_l - theta_r)/2

    x_dot = r_m*(theta_l_dot + theta_r_dot)/2
    y_dot = r_m*(theta_l_dot - theta_r_dot)/2
    return x, y, x_dot, y_dot

def state_space_decoupled():
    A_x = np.array([[0, 1, 0], [0, -(8*mu_r + r_m*r_m*mu_lx)/(m*r_m*r_m + 2*J_m), (2*r_m*K_m)/(m*r_m*r_m + 2*J_m)], [0, -K_m/(r_m*L_m), -R_m/L_m]])

    A_y = np.array([[0, 1, 0], [0, -(8*mu_r + r_m*r_m*mu_ly)/(m*r_m*r_m + 2*J_m), (2*r_m*K_m)/(m*r_m*r_m + 2*J_m)], [0, -K_m/(r_m*L_m), -R_m/L_m]])

    B = np.expand_dims(np.array([0, 0, 1/L_m]).T, 1)
    C = np.expand_dims(np.array([1, 0, 0]), 0)
    D = np.array([0])

    return ss(A_x, B, C, D), ss(A_y, B, C, D)

P = 20
omega = 2*np.pi/P
t = np.linspace(0, 3*P, 500)
u_ellipse = np.sin(omega*t)
v_ellipse = np.cos(omega*t)

u_square = np.repeat([1, 0, -1, 0, 1], 100)
v_square = np.repeat([0, 1, 0, -1, 0], 100)

ssx, ssy = state_space_decoupled()

plt.plot(ssx.forced_response(t, u_ellipse).outputs[2*P:], ssy.forced_response(t, v_ellipse).outputs[2*P:])
plt.figure()
plt.plot(ssx.forced_response(t, u_square).outputs, ssy.forced_response(t, v_square).outputs)
plt.show()


    
