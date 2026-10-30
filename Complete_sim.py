import numpy as np
import matplotlib.pyplot as plt
import draw_shape

bed = 0.25     # assumed side-length of the printing area (taken as a square) [m]
spool = 0.4     # lenght of each spool (really short so we see some spool changes) [m]

t = np.linspace(0, 60, 500)

ssx, ssy = draw_shape.state_space_decoupled()

u_right, v_right = draw_shape.inputs_from_voltages(1, 1)
u_left, v_left = draw_shape.inputs_from_voltages(-1, -1)
u_up, v_up = draw_shape.inputs_from_voltages(1, -1)
u_down, v_down = draw_shape.inputs_from_voltages(-1, 1)

right = (np.fmin(ssx.forced_response(t, u_right).outputs, bed), np.fmin(ssy.forced_response(t, v_right).outputs, bed))
left = (np.fmax(ssx.forced_response(t, u_left).outputs, -bed), np.fmin(ssy.forced_response(t, v_left).outputs, bed))
up = (np.fmin(ssx.forced_response(t, u_up).outputs, bed), np.fmin(ssy.forced_response(t, v_up).outputs, bed))
down = (np.fmin(ssx.forced_response(t, u_down).outputs, bed), np.fmax(ssy.forced_response(t, v_down).outputs, -bed))

plot_x = [[0], []]          # The printer can do maximum 2 colours
plot_y = [[0], []]

parking_states = ["not parked", "bottom", "top", "right", "left", "parked"]
parking_state = "not parked"
parked = False

spool_states = ["Printing", "Not printing"] # 2.1 is simplified, as spool change procedure is not simulated
spool_inputs = ["C", "F", "None"]
spool_state = "Printing"
spool_input = "None"
colour = 0
direction = [right, up, left, down]

instruction = 0
last_location = [0, 0]
printed_distance = 0.0

i = 1
while i < 500:
    dx = direction[instruction][0][i] - direction[instruction][0][i-1]
    dy = direction[instruction][1][i] - direction[instruction][1][i-1]
    x = last_location[0] + dx
    y = last_location[1] + dy
    last_location =[x, y]
    printed_distance += np.sqrt(dx*dx + dy*dy)
    
    if np.abs(dx) < 0.0000001:
        if instruction == 0:
            parking_state = "right"
        elif instruction == 2:
            parking_state = "left"
            parked = True

    if np.abs(dy) < 0.0000001:
        if instruction == 1:
            parking_state = "top"
            parked = False
        elif instruction == 3:
            parking_state = "bottom"
            if parked:
                parked = True
            else:
                parked = False

    if parking_state == "right" and instruction == 0:
        instruction = 1
        i = 0
    elif parking_state == "top" and instruction == 1:
        instruction = 2
        i = 0
        spool_input = "C"
    elif parking_state == "left" and instruction == 2:
        instruction = 3
        i = 0
    elif parking_state == "bottom" and instruction == 3:
        i = 1000

    if printed_distance > spool:
        spool_input = "F"

    if spool_input != "None":
        spool_state = "Not printing"
        plot_x[colour].append(0.0)
        plot_y[colour].append(0.0)
        if spool_input == "C":
            colour = (colour + 1)%2
        printed_distance = 0.0
        spool_state = "Printing"
        spool_input = "None"



    plot_x[colour].append(x)
    plot_y[colour].append(y)

    print(i, printed_distance, dx, dy, parking_state, instruction)
     
    i += 1
     


plt.plot(plot_x[0], plot_y[0])
plt.plot(plot_x[1], plot_y[1])
plt.show()
