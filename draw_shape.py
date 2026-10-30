import numpy as np
import matplotlib.pyplot as plt
from control import ss 

# parameters (fully made up)
r_m = 0.04         # m   
mu_r = 0.1
mu_lx = 0.1
mu_ly = 0.1
K_m = 1 
J_m = 1
R_m = 1
L_m = 1
m = 0.5         # kg


def inputs_from_voltages(uml, umr):
    """Converts from motor voltages to decoupled state-space system inputs"""
    u = (uml + umr)/2
    v = (uml - umr)/2
    return u, v


def kinematics(theta_l, theta_r, theta_l_dot, theta_r_dot, x0, y0):
    """Converts from motor rotation to nozzle translation"""
    x = x0 + r_m*(theta_l + theta_r)/2
    y = y0 + r_m*(theta_l - theta_r)/2

    x_dot = r_m*(theta_l_dot + theta_r_dot)/2
    y_dot = r_m*(theta_l_dot - theta_r_dot)/2
    return x, y, x_dot, y_dot

def state_space_decoupled():
    """See equations in the report """
    A_x = np.array([[0, 1, 0], [0, -(8*mu_r + r_m*r_m*mu_lx)/(m*r_m*r_m + 2*J_m), (2*r_m*K_m)/(m*r_m*r_m + 2*J_m)], [0, -K_m/(r_m*L_m), -R_m/L_m]])

    A_y = np.array([[0, 1, 0], [0, -(8*mu_r + r_m*r_m*mu_ly)/(m*r_m*r_m + 2*J_m), (2*r_m*K_m)/(m*r_m*r_m + 2*J_m)], [0, -K_m/(r_m*L_m), -R_m/L_m]])

    B = np.expand_dims(np.array([0, 0, 1/L_m]).T, 1)
    C = np.expand_dims(np.array([1, 0, 0]), 0)
    D = np.array([0])

    return ss(A_x, B, C, D), ss(A_y, B, C, D)

if __name__ == "__main__":
    P = 20
    omega = 2*np.pi/P
    t = np.linspace(0, 3*P, 500)

    uml_ellipse = np.sin(omega*t) + np.cos(omega*t)         # motor voltages for ellipse
    umr_ellipse = np.sin(omega*t) - np.cos(omega*t)

    u_ellipse, v_ellipse = inputs_from_voltages(uml_ellipse, umr_ellipse)       # inputs for making an ellipse
    
    uml_square = np.repeat([1, 1, -1, -1, 1], 100)      # motor voltages for square
    umr_square = np.repeat([1, -1, -1, 1, 1], 100)
    u_square, v_square = inputs_from_voltages(uml_square, umr_square)           # inputs for making a square
    
    ssx, ssy = state_space_decoupled()
    
    plt.plot(ssx.forced_response(t, u_ellipse).outputs[2*P:], ssy.forced_response(t, v_ellipse).outputs[2*P:])           # the printer head moves around a couple laps before starting printing. I found that this makes the ellipse nicer (some transient effects in the step-response probably)
    plt.figure()
    plt.plot(ssx.forced_response(t, u_square).outputs, ssy.forced_response(t, v_square).outputs)            # the corners are impossible to get right!
    plt.show()
    
    
        
