import numpy as np
import matplotlib.pyplot as plt
import draw_shape

bed = 0.25     # assumed side-length of the printing area (taken as a square) [m]
spool = 0.4     # lenght of each spool (really short so we see some spool changes) [m]

t = np.linspace(0, 60, 500)     # time array for the state-space system

ssx, ssy = draw_shape.state_space_decoupled()       # the state-space model of the system from Q1

u_right, v_right = draw_shape.inputs_from_voltages(1, 1)        # The inputs are the actual motor voltages, in this case (1, 1)
u_left, v_left = draw_shape.inputs_from_voltages(-1, -1)
u_up, v_up = draw_shape.inputs_from_voltages(1, -1)
u_down, v_down = draw_shape.inputs_from_voltages(-1, 1)

right = (np.fmin(ssx.forced_response(t, u_right).outputs, bed), np.fmin(ssy.forced_response(t, v_right).outputs, bed))        # the fmin and fmax are simulated walls
left = (np.fmax(ssx.forced_response(t, u_left).outputs, -bed), np.fmin(ssy.forced_response(t, v_left).outputs, bed))        # Arrays simulating the printer heat bashing against the walls
up = (np.fmin(ssx.forced_response(t, u_up).outputs, bed), np.fmin(ssy.forced_response(t, v_up).outputs, bed))     #Parking detector automaton where are you?
down = (np.fmin(ssx.forced_response(t, u_down).outputs, bed), np.fmax(ssy.forced_response(t, v_down).outputs, -bed))

plot_x = [[0], []]          # The printer can do maximum 2 colours
plot_y = [[0], []]

# parking_states = ["not parked", "bottom", "top", "right", "left", "parked"]
parking_state = "not parked"
parked = False          # it makes the automaton states easier to update

#spool_states = ["Printing", "Not printing"] # 2.1 is simplified, as specific spool change procedure is not simulated
#spool_inputs = ["C", "F", "None"]
spool_state = "Printing"
spool_input = "None"
colour = 0
direction = [right, up, left, down]         # that's all you need for a square (for fancy shapes, redefine direction as a different list)

instruction = 0
last_location = [0, 0]              # thats actually only needed when the parking detector automaton remembers the input, but I update it also in the Printing state, because I need it for the simulation
printed_distance = 0.0

i = 1
while i < 500:
    # instantaneous displacement (is in the same direction as instantaneous velocity)
    dx = direction[instruction][0][i] - direction[instruction][0][i-1]
    dy = direction[instruction][1][i] - direction[instruction][1][i-1]
    
    # location
    x = last_location[0] + dx
    y = last_location[1] + dy
    last_location =[x, y]


    printed_distance += np.sqrt(dx*dx + dy*dy)
    
    # states of the parking detector (the inputs are not quite as {V,H} x {0, +}, but this is easier to code)
    if np.abs(dx) < 0.0000001:
        if instruction == 0:
            parking_state = "right"         # the parking detector is expanded for all 4 sides, to stop the printer head from getting stuck at the walls (so we can make a perfect square)
        elif instruction == 2:
            parking_state = "left"
            parked = True               # that helpful variable (again not part of the automaton but it helps with the coding)

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
        instruction = 1         # go up
        i = 0
    elif parking_state == "top" and instruction == 1:
        instruction = 2         # now go left
        i = 0
        spool_input = "C"
    elif parking_state == "left" and instruction == 2:
        instruction = 3         # now go down again
        i = 0
    elif parking_state == "bottom" and instruction == 3:
        i = 1000                # Stop, the square is finished

    if printed_distance > spool:            # spool ran out
        spool_input = "F"

    if spool_input != "None":
        spool_state = "Not printing"        # This would be 2 steps in the FSM, but I can combine them because I can represent "not none" in python while storing the real state inside spool_input, but this does not work in the FSM
        plot_x[colour].append(0.0)
        plot_y[colour].append(0.0)
        if spool_input == "C":
            colour = (colour + 1)%2         # switch to the other colour
        printed_distance = 0.0              # new spool
        spool_state = "Printing"
        spool_input = "None"



    plot_x[colour].append(x)
    plot_y[colour].append(y)

    i += 1
     


plt.plot(plot_x[0], plot_y[0])
plt.plot(plot_x[1], plot_y[1])
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.show()
