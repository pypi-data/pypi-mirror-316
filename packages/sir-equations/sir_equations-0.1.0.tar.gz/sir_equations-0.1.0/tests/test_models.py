import pytest
import numpy as np
from sir_equations.main import EpiModel, GASModel, run_simulation

def test_sir_conservation():
    """Test conservation of population in SIR model"""
    model = EpiModel(a=0.3, b=0.1, initial_conditions=[0.99, 0.01, 0])
    t, solution = run_simulation(model, t_span=100, t_points=1000)
    
    for s in solution:
        assert abs(sum(s) - 1.0) < 1e-10

def test_gas_conservation():
    """Test conservation of population in GAS model"""
    model = GASModel(
        a=0.3, b=0.1, k=0.2, Ip=0.02,
        transition_rates=[1/50, 1/100],
        initial_conditions=[0.99, 0.01, 0]
    )
    t, solution = run_simulation(model, t_span=100, t_points=1000)
    
    for s in solution:
        assert abs(sum(s) - 1.0) < 1e-10