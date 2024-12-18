import numpy as np
from scipy.integrate import odeint
import pandas as pd

class EpiModel:
    """Base epidemiological model implementing classical SIR dynamics"""
    
    def __init__(self, a, b, initial_conditions):
        self.a = a  # infection rate
        self.b = b  # recovery rate
        self.S0, self.I0, self.R0 = initial_conditions
    
    def sir_equations(self, state, t):
        """Basic SIR model differential equations"""
        S, I, R = state
        # dS/dt = -aSI
        dSdt = -self.a * S * I
        # dI/dt = aSI - bI
        dIdt = self.a * S * I - self.b * I
        # dR/dt = bI
        dRdt = self.b * I
        return [dSdt, dIdt, dRdt]

class GASModel(EpiModel):
    """Extended model incorporating GAS (General Adaptation Syndrome) theory"""
    
    def __init__(self, a, b, k, Ip, transition_rates, initial_conditions):
        super().__init__(a, b, initial_conditions)
        self.k = k  # crowd effect parameter
        self.Ip = Ip  # media influence factor
        self.tr1 = transition_rates[0]  # Sres -> Sexh rate
        self.tr2 = transition_rates[1]  # Sexh -> Sign rate
        self.states = {
            'Sign': initial_conditions[0] * 0.8,
            'Sres': initial_conditions[0] * 0.15,
            'Sexh': initial_conditions[0] * 0.05
        }

    def extended_equations(self, state, t):
        """Extended differential equations including behavioral states"""
        Sign, Sres, Sexh, I, R = state
        
        # Crowd effect term
        crowd_effect = self.k * Sign * (I ** 2)
        
        # Media influence
        media_effect = self.Ip * I
        
        # State transitions
        dSigndt = -crowd_effect + self.tr2 * Sexh - media_effect
        dSresdt = -self.tr1 * Sres + media_effect
        dSexhdt = self.tr1 * Sres - self.tr2 * Sexh
        
        # Modified SIR equations
        dIdt = crowd_effect - self.b * I
        dRdt = self.b * I
        
        return [dSigndt, dSresdt, dSexhdt, dIdt, dRdt]

def run_simulation(model, t_span, t_points):
    """Run numerical integration of the model"""
    t = np.linspace(0, t_span, t_points)
    
    if isinstance(model, GASModel):
        initial_state = [model.states['Sign'], model.states['Sres'],
                        model.states['Sexh'], model.I0, model.R0]
        solution = odeint(model.extended_equations, initial_state, t)
    else:
        initial_state = [model.S0, model.I0, model.R0]
        solution = odeint(model.sir_equations, initial_state, t)
    
    return t, solution

def analyze_data(t, solution, model_type='SIR'):
    """Analyze simulation results"""
    if model_type == 'SIR':
        df = pd.DataFrame({
            'time': t,
            'S': solution[:, 0],
            'I': solution[:, 1],
            'R': solution[:, 2]
        })
    else:  # GAS model
        df = pd.DataFrame({
            'time': t,
            'Sign': solution[:, 0],
            'Sres': solution[:, 1],
            'Sexh': solution[:, 2],
            'I': solution[:, 3],
            'R': solution[:, 4]
        })
    
    # Calculate normalized cumulative data
    df['P'] = 1 - df[['Sign', 'Sres', 'Sexh']].sum(axis=1) if model_type == 'GAS' else 1 - df['S']
    
    return df