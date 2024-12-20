import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import odeintw as ow
import tqdm as tq

def sol_ode(model, var0, t, param):

    """
    Solves a system of ordinary differential equations (ODEs).
    
    Args:
        model (callable(var,t,param)): The function computes the derivative of y at t.
        var0 (array): Initial condition of var.
        t (array): A sequence of time points at which var is calculated.
        param (array): Model parameters.

    Returns:
        ar (array): Array containing the value of var for each desired time in t, with the initial value var0 in the first row.
    """
    
    dt = t[1]-t[0]
    if isinstance(param,list):
        if (len(param) == 1):
            param = param[0]
        else: pass
    else: pass

    if isinstance(var0,list):
        var0 = np.array(var0)
    else: pass
    
    results = ow.odeintw(model, y0=var0, t=t, args=(param,),hmax = dt)
    
    try:
        out = model(var0, t, param) #this is a workaround, so in the case of 1 variable and n CSTRs the result does not get flipped
    except ValueError:
        out = (1,1)
    
    if isinstance(out, tuple):
        m = int(np.shape(var0)[0])
        ar = list(range(m))
        for i in range(m):
            ar[i] = results[:,i]
    else:
        ar = results
    return ar