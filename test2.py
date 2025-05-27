from lcapy import Circuit
from sympy import symbols, pprint

circuit = Circuit("""
R1 0 1;up
R4 1 2;up
W 2 4;right
R3 4 5;down
L1 1 5;right
W 5 6;right
R2 6 7;up
W 6 8;down
C1 8 9;left
SW 9 0 nc 0;left
V1 4 7;right
""")

print("Converting circuit to IVP")

cct_ivp = circuit.convert_IVP(0)

print(cct_ivp)