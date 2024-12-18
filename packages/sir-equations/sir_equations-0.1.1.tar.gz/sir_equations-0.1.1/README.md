# Epidemiological Model with Social-Psychological Behavior

This package implements an advanced epidemiological modeling framework that combines traditional SIR (Susceptible-Infected-Recovered) dynamics with social-psychological behavior patterns based on General Adaptation Syndrome (GAS) theory. It's designed to provide deeper insights into disease transmission patterns by incorporating human behavioral responses during epidemics.

## Features
## Classical SIR Model
- Implementation of fundamental epidemiological equations
- Customizable infection and recovery rates
- Population conservation guarantees
- Numerical integration using advanced solvers
- Basic reproduction number (R0) calculations

## Extended GAS Model Integration

## Three distinct behavioral states:

- Ignorance (Sign)
- Resistance (Sres)
- Exhaustion (Sexh)


- State transition modeling
- Behavioral feedback mechanisms
- Time-dependent adaptation patterns

## Crowd Effect Modifications

- Superlinear alarm responses
- Population density considerations
- Social network effects
- Mass media influence factors
- Dynamic behavioral thresholds

## Advanced Analysis Tools

- Real-time simulation capabilities
- Data visualization utilities
- Parameter estimation functions
- Statistical analysis tools
- Cross-regional comparison frameworks

## Installation
pip install sir-equations

## Sample Code

from sir-equations import GASModel, run_simulation, analyze_data

# Create a model instance
model = GASModel(
    a=0.3,          # infection rate
    b=0.1,          # recovery rate
    k=0.2,          # crowd effect parameter
    Ip=0.02,        # media influence factor
    transition_rates=[1/50, 1/100],  # behavioral transition rates
    initial_conditions=[0.99, 0.01, 0]
)

# Run simulation
t, solution = run_simulation(model, t_span=100, t_points=1000)

# Analyze results
results = analyze_data(t, solution, model_type='GAS')