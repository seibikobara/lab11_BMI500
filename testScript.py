'''
This is a test script to run a simulation.
Below is a simulation for SEIR model.
'''

import matplotlib.pyplot as plt
import seirModel as seir

# Simulation
# parameter setting
params = {'alpha_e': 0.2,   # infectious rate from exposure
          'alpha_i': 0.8,   # infectious rate from infection
          'gamma'  : 1/100, # duration of immunity  
          'kappa': 1/7,     # incubation period
          'rho': 0.1,       # proportion of recovery from exposure 
          'beta':0.1,       # recovery rate
          'mu': 0.001}      # mortality among the infected

# inital setup
initials = {'st': 0.9999,   # proportion of individuals susceptible
            'et': 0,        # proportion of individuals exposed 
            'it':0.0001,    # proportion of individuals infected
            'rt': 0,        # proportion of individuals recovered
            'pt':0}         # proportion of individuals died

# simulation for a year
res = seir.SEIR_simulation(365,params, initials)

# visulalize
plt.plot(res['time'],res['st'],label='Proportion of susceptible')
plt.plot(res['time'],res['et'],label='Proportion of exposed')
plt.plot(res['time'],res['it'],label='Proportion of infectious')
plt.plot(res['time'],res['rt'],label='Proportion of recovered')
plt.plot(res['time'],res['pt'],label='Proportion of died')
plt.xlabel('Days')
plt.ylabel("Proportion")
plt.legend()
plt.title('SEIR model')
plt.show()
plt.close()