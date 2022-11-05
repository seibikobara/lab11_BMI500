

'''
This module aims to create a SEIR compartmental model.
This model uses paramters and proportion of each compartment.

Parameters are below:
alpha_e: Infectious rate from individuals who are exposured 
alpha_i: Infectious rate from individuals who are infected
gamma  : Duration of immunity after infection  
kappa  : Incubation period
rho    : Proportion of recovery from exposure
beta   : Recovery rate from infection 
mu     : Mortality among individuals who are infected

The proportion of each compartment are below:
st   : Proportion of individuals who are susceptible at a time
et   : Proportion of individuals who are exposed at a time
it   : Proportion of individuals who are infected at a time
rt   : Proportion of individuals who are recovered at a time
pt   : Proportion of individuals who have died at a time
'''

import numpy as np
import pandas as pd


# Model: SEIR model
# compartment update function
def seir_model_upddate(st,et,it,rt, params):
    # extract params
    alpha_e = params['alpha_e']
    alpha_i = params['alpha_i']
    gamma   = params['gamma']
    kappa   = params['kappa']
    rho     = params['rho']
    beta    = params['beta']
    mu      = params['mu']

    # differential equiations
    dst = -alpha_e* st*et -alpha_i* st*it + gamma*rt
    det = alpha_e* st*et + alpha_i* st*it -kappa*et - rho*et
    dit = kappa*et - beta*it -mu*it
    drt = beta*it + rho*et - gamma*rt
    dpt = mu*it 
    
    return dst, det, dit, drt, dpt 

# simulation function
def SEIR_simulation(days, params, initial_settings):
    
    # initial setting
    st  = initial_settings['st']
    et  = initial_settings['et']
    it  = initial_settings['it']
    rt  = initial_settings['rt']
    pt  = initial_settings['pt']
    
    # for storing values
    st_list = list()
    et_list = list()
    it_list = list()
    rt_list = list()
    pt_list = list()
    time_list = list()
    
    # simulation by a function of days
    for time in np.arange(0,days+1,1):  # a year
        # current st, et, it, rt, pt
        st_list = st_list + [st]
        et_list = et_list + [et]
        it_list = it_list + [it]
        rt_list = rt_list + [rt]
        pt_list = pt_list + [pt]
        time_list = time_list + [time]    
        # update
        dst, det, dit, drt, dpt = seir_model_upddate(st,et,it,rt, params)
        st += dst
        et += det
        it += dit
        rt += drt
        pt += dpt
    # summarize
    d = {'time': time_list,
         'st': st_list,
         'et': et_list,
         'it': it_list,
         'rt': rt_list,
         'pt': pt_list}
    res = pd.DataFrame(d)
    return res