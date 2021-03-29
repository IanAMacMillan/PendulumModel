'''
Author: Ian MacMillan
Date Started: March 2021
Purpose: create a model of a Pendulum to be used to simulate the LIGO system
'''

import numpy as np
import time
import os

def step(state, dt=0.05, add_noise=False):

    x, x_dot, theta, theta_dot, phi, phi_dot = state

    #u = np.clip(u, -self.max_torque, self.max_torque)[0]

    g = 9.81 #m/s
    
    #all from table 2 in T000134
    l = 0.442 # m
    b = 6.83 * 10 ** (-3) #m
    R1 = 1.67 * 10 ** (-2) #m
    R2 = 0.126 #m
    
    #all from table 3 in T000134
    m= 10.5 #kg
    I_phi = 4.98 * 10 ** (-2) #kg m^2 From eq 22
    I_theta = 4.98 * 10 ** (-2) #kg m^2 From eq 22
    
    #using Euler method for toy model
    new_x_dot = x_dot - (g/l * (x-b*theta)) * dt #from eq 26 in T000134
    new_x= x + new_x_dot*dt
    
    new_theta_dot = theta_dot + (1/I_theta) * (-m * g * b * theta + m * g * b/l * (x-b * theta)) * dt #from eq 27 in T000134
    new_theta = theta + new_theta_dot*dt

    new_phi_dot = phi_dot + (1/I_phi) * (-m * R1 * R2 * g/l * phi) * dt #from eq 28 in T000134
    new_phi = phi + new_phi_dot*dt
    
    output_state=np.array([new_x, new_x_dot, new_theta, new_theta_dot, new_phi, new_phi_dot])

    return output_state
    
def report(state, filename, print_data=False):
    x, x_dot, theta, theta_dot, phi, phi_dot = state
    save_string=str(x)+'\t'+str(x_dot)+'\t'+str(theta)+'\t'+str(theta_dot)+'\t'+str(phi)+'\t'+str(phi_dot)+'\n'
    
    if print_data==True:
        print(save_string)
    
    with open(filename, 'a') as the_file:
        towrite=save_string
        the_file.write(towrite)
            
def getfilename():
    pathtofolder='ModelData'
    entries = os.listdir(pathtofolder)
    highestrun=0
    for file in entries:
        if file!='.DS_Store':
            if int(file[4:-4])>=highestrun:
                highestrun=int(file[4:-4])+1
    filepath=pathtofolder+"/Run_"+str(highestrun)+".txt"
    return filepath
        
def reset(state):
    #if state==None:
    #    state=np.array([0,0,0,0,0,0])
    return state
    


#To test these functions
#input_state=[ul,ur,ll,lr]

x_data=[]
t_data=[]

filename=getfilename()
print(filename)
state=reset(np.array([0,0,0,0,0.5,0]))
report(state, filename, print_data=False)
for i in range(1000):
    state=step(state)
    report(state, filename, print_data=False)
    x, x_dot, theta, theta_dot, phi, phi_dot = state
    
    x_data.append(x) #replace x with a diffrent varible to see its value over time
    t_data.append(i*0.05)

import matplotlib.pyplot as plt
plt.plot(t_data, x_data)
plt.ylabel('x value (m)')
plt.xlabel('Time (s)')
plt.show()
